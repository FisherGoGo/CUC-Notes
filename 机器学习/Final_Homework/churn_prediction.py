# -*- coding: utf-8 -*-
"""
视频平台用户流失预测 —— 期末大作业
基于机器学习分类算法的用户流失预测模型
使用多种分类算法预测用户是否会流失（is_active = False）
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime

print("=" * 60)
print("视频平台用户流失预测系统")
print("=" * 60)

# ============================================================
# 第1部分：数据加载
# ============================================================
print("\n[1/7] 加载数据...")
df_users = pd.read_csv('movies_dataset/1.csv')
df_movies = pd.read_csv('movies_dataset/2.csv')
df_watch = pd.read_csv('movies_dataset/3.csv')
df_reviews = pd.read_csv('movies_dataset/4.csv')
df_search = pd.read_csv('movies_dataset/5.csv')
df_rec = pd.read_csv('movies_dataset/6.csv')

print(f"  用户表: {df_users.shape[0]}条, 影视表: {df_movies.shape[0]}条, "
      f"观看: {df_watch.shape[0]}条, 评论: {df_reviews.shape[0]}条")
print(f"  搜索: {df_search.shape[0]}条, 推荐: {df_rec.shape[0]}条")

# 目标变量分布
print(f"\n  目标变量 is_active: True={df_users['is_active'].sum()}, "
      f"False={(~df_users['is_active']).sum()} (流失率: {1-df_users['is_active'].mean():.1%})")

# ============================================================
# 第2部分：特征工程
# ============================================================
print("\n[2/7] 特征工程...")
REFERENCE_DATE = pd.Timestamp('2026-05-01')

# --- 2.1 清洗用户表 ---
df_users['age_clean'] = df_users['age'].copy()
df_users.loc[(df_users['age_clean'] < 0) | (df_users['age_clean'] > 100), 'age_clean'] = np.nan
age_median = df_users['age_clean'].median()
df_users['age_clean'].fillna(age_median, inplace=True)

df_users['household_size'].fillna(df_users['household_size'].median(), inplace=True)
df_users['monthly_spend'] = df_users.groupby('subscription_plan')['monthly_spend'].transform(
    lambda x: x.fillna(x.median()))
df_users['gender'].fillna('Unknown', inplace=True)

df_users['created_at'] = pd.to_datetime(df_users['created_at'])
df_users['account_age_days'] = (REFERENCE_DATE - df_users['created_at']).dt.days
df_users['subscription_start_date'] = pd.to_datetime(df_users['subscription_start_date'])
df_users['subscription_days'] = (REFERENCE_DATE - df_users['subscription_start_date']).dt.days

# 月消费占订阅时长的比率（消费效率）
df_users['spend_per_sub_day'] = df_users['monthly_spend'] / (df_users['subscription_days'] / 30 + 1)

# 基础特征DataFrame
df_feat = df_users[['user_id', 'is_active']].copy()
df_feat['age'] = df_users['age_clean']
df_feat['household_size'] = df_users['household_size']
df_feat['monthly_spend'] = df_users['monthly_spend']
df_feat['account_age_days'] = df_users['account_age_days']
df_feat['subscription_days'] = df_users['subscription_days']
df_feat['spend_per_sub_day'] = df_users['spend_per_sub_day']

# One-Hot编码
for col in ['gender', 'country', 'subscription_plan', 'primary_device']:
    dummies = pd.get_dummies(df_users[col], prefix=col, drop_first=True)
    df_feat = pd.concat([df_feat, dummies], axis=1)

# --- 2.2 观看行为特征 ---
df_watch['watch_date'] = pd.to_datetime(df_watch['watch_date'])
watch_agg = df_watch.groupby('user_id').agg(
    total_sessions=('session_id', 'count'),
    total_duration=('watch_duration_minutes', 'sum'),
    avg_duration=('watch_duration_minutes', 'mean'),
    std_duration=('watch_duration_minutes', 'std'),
    avg_progress=('progress_percentage', 'mean'),
    std_progress=('progress_percentage', 'std'),
    completion_rate=('action', lambda x: (x == 'completed').mean()),
    started_rate=('action', lambda x: (x == 'started').mean()),
    paused_rate=('action', lambda x: (x == 'paused').mean()),
    unique_movies=('movie_id', 'nunique'),
    unique_devices=('device_type', 'nunique'),
    download_rate=('is_download', 'mean'),
    hd_rate=('quality', lambda x: (x == 'HD').mean()),
    first_watch=('watch_date', 'min'),
    last_watch=('watch_date', 'max'),
    avg_user_rating=('user_rating', 'mean'),
    rating_count=('user_rating', 'count'),
).reset_index()

watch_agg['watch_days_span'] = (watch_agg['last_watch'] - watch_agg['first_watch']).dt.days
watch_agg['days_since_last_watch'] = (REFERENCE_DATE - watch_agg['last_watch']).dt.days
watch_agg['avg_user_rating'].fillna(0, inplace=True)
watch_agg['std_duration'].fillna(0, inplace=True)
watch_agg['std_progress'].fillna(0, inplace=True)
watch_agg['watch_frequency'] = watch_agg['total_sessions'] / (watch_agg['watch_days_span'] + 1)

df_feat = df_feat.merge(
    watch_agg.drop(columns=['first_watch', 'last_watch']), on='user_id', how='left')

# --- 2.3 评论行为特征 ---
df_reviews['review_date'] = pd.to_datetime(df_reviews['review_date'])
review_agg = df_reviews.groupby('user_id').agg(
    total_reviews=('review_id', 'count'),
    avg_review_rating=('rating', 'mean'),
    positive_rate=('sentiment', lambda x: (x == 'positive').mean()),
    negative_rate=('sentiment', lambda x: (x == 'negative').mean()),
    avg_sentiment_score=('sentiment_score', 'mean'),
    verified_watch_rate=('is_verified_watch', 'mean'),
    total_helpful=('helpful_votes', 'sum'),
    total_votes_all=('total_votes', 'sum'),
).reset_index()
review_agg['helpfulness_ratio'] = np.where(
    review_agg['total_votes_all'] > 0,
    review_agg['total_helpful'] / review_agg['total_votes_all'], 0)
review_agg['avg_sentiment_score'].fillna(0, inplace=True)

df_feat = df_feat.merge(
    review_agg.drop(columns=['total_helpful', 'total_votes_all']), on='user_id', how='left')

# --- 2.4 搜索行为特征 ---
df_search['search_date'] = pd.to_datetime(df_search['search_date'])
search_agg = df_search.groupby('user_id').agg(
    total_searches=('search_id', 'count'),
    avg_results=('results_returned', 'mean'),
    typo_rate=('had_typo', 'mean'),
    filter_usage_rate=('used_filters', 'mean'),
    avg_search_duration=('search_duration_seconds', 'mean'),
    avg_click_position=('clicked_result_position', 'mean'),
).reset_index()
search_agg['avg_click_position'].fillna(0, inplace=True)
search_agg['avg_search_duration'].fillna(0, inplace=True)

df_feat = df_feat.merge(search_agg, on='user_id', how='left')

# --- 2.5 推荐行为特征 ---
df_rec['recommendation_date'] = pd.to_datetime(df_rec['recommendation_date'])
rec_agg = df_rec.groupby('user_id').agg(
    total_recommendations=('recommendation_id', 'count'),
    rec_click_rate=('was_clicked', 'mean'),
    avg_rec_score=('recommendation_score', 'mean'),
    avg_rec_position=('position_in_list', 'mean'),
    evening_rec_rate=('time_of_day', lambda x: (x == 'evening').mean()),
    personalized_rec_rate=('recommendation_type', lambda x: (x == 'personalized').mean()),
).reset_index()
rec_agg['avg_rec_score'].fillna(0, inplace=True)

df_feat = df_feat.merge(rec_agg, on='user_id', how='left')

# --- 2.6 用户对电影类型的偏好特征 ---
# 用户观看电影的主要类型
user_watch_with_genre = df_watch[['user_id', 'movie_id']].merge(
    df_movies[['movie_id', 'genre_primary']], on='movie_id', how='left')
user_genre_counts = user_watch_with_genre.groupby(['user_id', 'genre_primary']).size().reset_index(name='count')
user_top_genre = user_genre_counts.loc[user_genre_counts.groupby('user_id')['count'].idxmax()]
user_top_genre = user_top_genre.rename(columns={'genre_primary': 'top_genre'})
genre_dummies = pd.get_dummies(user_top_genre['top_genre'], prefix='fav_genre')
genre_feat = pd.concat([user_top_genre[['user_id']], genre_dummies], axis=1)
df_feat = df_feat.merge(genre_feat, on='user_id', how='left')

# --- 2.7 全局填充 ---
for col in df_feat.columns:
    if col not in ['user_id', 'is_active'] and df_feat[col].dtype in ['float64', 'int64']:
        df_feat[col].fillna(0, inplace=True)
    elif col not in ['user_id', 'is_active'] and df_feat[col].dtype == 'bool':
        df_feat[col].fillna(False, inplace=True)

print(f"  特征矩阵: {df_feat.shape}, 缺失值: {df_feat.isnull().sum().sum()}")

# ============================================================
# 第3部分：探索性数据分析 (EDA)
# ============================================================
print("\n[3/7] 探索性数据分析与可视化...")

X = df_feat.drop(columns=['user_id', 'is_active'])
y = df_feat['is_active'].astype(int)
feature_names = X.columns.tolist()

# 相关性分析
correlations = []
for col in feature_names:
    corr = np.corrcoef(X[col].values, y.values)[0, 1]
    correlations.append({'feature': col, 'correlation': corr})
corr_df = pd.DataFrame(correlations).sort_values('correlation', key=abs, ascending=False)
print(f"  与流失相关性Top 10: {corr_df.head(10)['feature'].tolist()}")

# ---- EDA图1: 综合概览 ----
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# (1) 流失分布饼图
ax = axes[0, 0]
churn_counts = df_users['is_active'].value_counts()
ax.pie([churn_counts.get(True, 0), churn_counts.get(False, 0)],
       labels=['未流失', '已流失'], autopct='%1.1f%%',
       colors=['#2ecc71', '#e74c3c'], startangle=90, explode=(0, 0.05))
ax.set_title('用户流失分布', fontsize=14, fontweight='bold')

# (2) 订阅计划流失率
ax = axes[0, 1]
churn_plan = df_users.groupby('subscription_plan')['is_active'].agg(
    ['count', lambda x: (1-x.mean())*100])
churn_plan.columns = ['count', 'churn_rate']
churn_plan = churn_plan.sort_values('churn_rate', ascending=False)
bars = ax.bar(range(len(churn_plan)), churn_plan['churn_rate'].values,
              color=['#e74c3c', '#f39c12', '#3498db', '#2ecc71'])
ax.set_xticks(range(len(churn_plan)))
ax.set_xticklabels(churn_plan.index, rotation=30, ha='right')
ax.set_title('各订阅计划流失率', fontsize=14, fontweight='bold')
ax.set_ylabel('流失率 (%)')
for i, v in enumerate(churn_plan['churn_rate'].values):
    ax.text(i, v + 0.3, f'{v:.1f}%', ha='center', fontsize=10)

# (3) 设备类型流失率
ax = axes[0, 2]
churn_device = df_users.groupby('primary_device')['is_active'].apply(
    lambda x: (1-x.mean())*100).sort_values()
ax.barh(range(len(churn_device)), churn_device.values, color='#e74c3c', alpha=0.8)
ax.set_yticks(range(len(churn_device)))
ax.set_yticklabels(churn_device.index)
ax.set_title('各设备类型流失率', fontsize=14, fontweight='bold')
ax.set_xlabel('流失率 (%)')
for i, v in enumerate(churn_device.values):
    ax.text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=9)

# (4) 年龄分布
ax = axes[1, 0]
active_age = df_users[df_users['is_active']]['age_clean']
churned_age = df_users[~df_users['is_active']]['age_clean']
ax.hist(active_age, bins=30, alpha=0.6, label='未流失', color='#2ecc71', edgecolor='white', density=True)
ax.hist(churned_age, bins=30, alpha=0.6, label='已流失', color='#e74c3c', edgecolor='white', density=True)
ax.set_title('年龄分布对比', fontsize=14, fontweight='bold')
ax.set_xlabel('年龄'), ax.set_ylabel('密度'), ax.legend()

# (5) 月消费分布
ax = axes[1, 1]
ax.hist(df_users[df_users['is_active']]['monthly_spend'], bins=30, alpha=0.6,
        label='未流失', color='#2ecc71', edgecolor='white', density=True)
ax.hist(df_users[~df_users['is_active']]['monthly_spend'], bins=30, alpha=0.6,
        label='已流失', color='#e74c3c', edgecolor='white', density=True)
ax.set_title('月消费分布对比', fontsize=14, fontweight='bold')
ax.set_xlabel('月消费'), ax.set_ylabel('密度'), ax.legend()

# (6) 账户年龄 vs 流失
ax = axes[1, 2]
temp = df_feat.copy()
temp['age_bucket'] = pd.cut(temp['account_age_days'], bins=6)
churn_age_bucket = temp.groupby('age_bucket', observed=False).apply(
    lambda x: (1 - x['is_active'].mean()) * 100)
ax.plot(range(len(churn_age_bucket)), churn_age_bucket.values, 'o-',
        color='#e74c3c', lw=2, markersize=8)
ax.set_xticks(range(len(churn_age_bucket)))
ax.set_xticklabels([str(b) for b in churn_age_bucket.index], rotation=30, ha='right', fontsize=7)
ax.set_title('流失率随账户年龄变化', fontsize=14, fontweight='bold')
ax.set_ylabel('流失率 (%)'), ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('results_overview.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] results_overview.png")

# ---- EDA图2: 特征相关性热力图 ----
top15 = corr_df.head(15)['feature'].tolist()
corr_matrix = X[top15].copy()
corr_matrix['churn'] = 1 - y  # churn=1表示流失

fig, ax = plt.subplots(figsize=(14, 12))
sns.heatmap(corr_matrix.corr(), annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            ax=ax, square=True, linewidths=0.5, annot_kws={'size': 7})
ax.set_title('特征相关性热力图 (Top15特征 + 流失标签)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] correlation_heatmap.png")

# ============================================================
# 第4部分：数据准备（SMOTE + 标准化）
# ============================================================
print("\n[4/7] 数据准备与SMOTE过采样...")

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                              roc_auc_score, classification_report, confusion_matrix,
                              roc_curve, precision_recall_curve, average_precision_score)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE

# 划分训练/测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SMOTE过采样（仅在训练集上）
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)

print(f"  训练集: {X_train.shape[0]} -> SMOTE后: {X_train_balanced.shape[0]}")
print(f"  SMOTE后类别分布: 0(流失)={sum(y_train_balanced==0)}, 1(未流失)={sum(y_train_balanced==1)}")

# ============================================================
# 第5部分：模型训练与超参数调优
# ============================================================
print("\n[5/7] 模型训练与评估...")

models = {
    '逻辑回归': LogisticRegression(max_iter=3000, random_state=42),
    '支持向量机(SVM)': SVC(kernel='rbf', probability=True, random_state=42),
    '朴素贝叶斯': GaussianNB(var_smoothing=1e-9),
    'K近邻(KNN)': KNeighborsClassifier(n_neighbors=5, weights='distance'),
    '随机森林': RandomForestClassifier(n_estimators=200, max_depth=10,
                                        min_samples_split=5, random_state=42),
    '梯度提升': GradientBoostingClassifier(n_estimators=150, max_depth=5,
                                            learning_rate=0.05, random_state=42),
    '神经网络(MLP)': MLPClassifier(hidden_layer_sizes=(128, 64, 32), activation='relu',
                                    max_iter=800, random_state=42, early_stopping=True,
                                    validation_fraction=0.1, n_iter_no_change=15),
}

results = {}
for name, model in models.items():
    print(f"  训练 {name} ...", end=' ')
    model.fit(X_train_balanced, y_train_balanced)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # 寻找最佳阈值 (最大化F1)
    best_f1, best_thresh = 0, 0.5
    for thresh in np.arange(0.15, 0.85, 0.02):
        temp_pred = (y_prob >= thresh).astype(int)
        temp_f1 = f1_score(y_test, temp_pred, zero_division=0)
        if temp_f1 > best_f1:
            best_f1, best_thresh = temp_f1, thresh

    # 使用最佳阈值
    y_pred_opt = (y_prob >= best_thresh).astype(int)

    acc = accuracy_score(y_test, y_pred_opt)
    prec = precision_score(y_test, y_pred_opt, zero_division=0)
    rec = recall_score(y_test, y_pred_opt, zero_division=0)
    f1 = f1_score(y_test, y_pred_opt, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)
    auprc = average_precision_score(y_test, y_prob)

    results[name] = {
        'model': model, 'accuracy': acc, 'precision': prec,
        'recall': rec, 'f1_score': f1, 'auc': auc, 'auprc': auprc,
        'y_pred': y_pred_opt, 'y_prob': y_prob, 'best_threshold': best_thresh,
    }
    print(f"Acc={acc:.3f} Prec={prec:.3f} Rec={rec:.3f} F1={f1:.3f} AUC={auc:.3f} AUPRC={auprc:.3f} Th={best_thresh:.2f}")

# ============================================================
# 第6部分：模型对比
# ============================================================
print("\n[6/7] 模型性能对比...")

results_df = pd.DataFrame([
    {'模型': n, '准确率': r['accuracy'], '精确率': r['precision'],
     '召回率': r['recall'], 'F1分数': r['f1_score'],
     'AUC': r['auc'], 'AUPRC': r['auprc'], '最佳阈值': r['best_threshold']}
    for n, r in results.items()
]).sort_values('F1分数', ascending=False)

print("\n>>> 模型性能汇总表 <<<")
print(results_df.to_string(index=False))
best_model = results_df.iloc[0]['模型']
print(f"\n最佳模型: {best_model} (F1={results_df.iloc[0]['F1分数']:.4f})")

# ============================================================
# 第7部分：结果可视化
# ============================================================
print("\n[7/7] 生成可视化图表...")

# --- 模型性能对比 ---
fig, ax = plt.subplots(figsize=(14, 7))
x_pos = np.arange(len(results_df))
width = 0.13
metrics_list = ['准确率', '精确率', '召回率', 'F1分数', 'AUC', 'AUPRC']
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
for i, (metric, color) in enumerate(zip(metrics_list, colors)):
    ax.bar(x_pos + i * width, results_df[metric].values, width, label=metric, color=color, alpha=0.85)
ax.set_xticks(x_pos + width * 2.5)
ax.set_xticklabels(results_df['模型'].values, rotation=25, ha='right', fontsize=9)
ax.set_ylabel('分数'), ax.set_ylim(0, 1.05)
ax.set_title('各模型性能指标对比', fontsize=14, fontweight='bold')
ax.legend(loc='lower right', fontsize=8, ncol=3)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] model_comparison.png")

# --- ROC曲线 ---
fig, ax = plt.subplots(figsize=(8, 7))
roc_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']
for idx, (name, r) in enumerate(results.items()):
    fpr, tpr, _ = roc_curve(y_test, r['y_prob'])
    ax.plot(fpr, tpr, lw=2, color=roc_colors[idx % len(roc_colors)],
            label=f"{name} (AUC={r['auc']:.3f})")
ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
ax.set_xlabel('假正率 (FPR)'), ax.set_ylabel('真正率 (TPR)')
ax.set_title('ROC曲线对比', fontsize=14, fontweight='bold')
ax.legend(fontsize=8, loc='lower right'), ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('roc_curves.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] roc_curves.png")

# --- PR曲线 ---
fig, ax = plt.subplots(figsize=(8, 7))
for idx, (name, r) in enumerate(results.items()):
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, r['y_prob'])
    ax.plot(recall_curve, precision_curve, lw=2, color=roc_colors[idx % len(roc_colors)],
            label=f"{name} (AUPRC={r['auprc']:.3f})")
ax.set_xlabel('召回率 (Recall)'), ax.set_ylabel('精确率 (Precision)')
ax.set_title('Precision-Recall曲线对比', fontsize=14, fontweight='bold')
ax.legend(fontsize=8), ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('pr_curves.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] pr_curves.png")

# --- 混淆矩阵（前3模型）---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
top3 = results_df.head(3)
for idx, (_, row) in enumerate(top3.iterrows()):
    name = row['模型']
    cm = confusion_matrix(y_test, results[name]['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                xticklabels=['预测流失', '预测未流失'],
                yticklabels=['实际流失', '实际未流失'])
    axes[idx].set_title(f'{name}\nF1={row["F1分数"]:.3f} AUC={row["AUC"]:.3f}', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('真实标签'), axes[idx].set_xlabel('预测标签')
plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] confusion_matrices.png")

# --- 特征重要性（随机森林）---
if '随机森林' in results:
    rf_model = results['随机森林']['model']
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[-20:]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(range(len(indices)), importances[indices], color='#3498db', alpha=0.85)
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices], fontsize=9)
    ax.set_xlabel('特征重要性 (Gini Importance)')
    ax.set_title('随机森林 - Top 20 特征重要性', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] feature_importance.png")

    print("\n>>> 随机森林 Top 20 重要特征:")
    for i in indices[::-1]:
        print(f"    {feature_names[i]:45s}: {importances[i]:.4f}")

# --- 流失率与关键特征的关系 ---
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

key_features = ['completion_rate', 'days_since_last_watch', 'avg_progress',
                'total_sessions', 'rec_click_rate', 'download_rate']
key_labels = ['完成率', '距最后观看天数', '平均观看进度',
              '总观看次数', '推荐点击率', '下载率']

for ax, feat, label in zip(axes.flatten(), key_features, key_labels):
    temp = df_feat[[feat, 'is_active']].copy()
    temp[feat].fillna(0, inplace=True)
    # 分箱
    if temp[feat].nunique() > 10:
        temp['bin'] = pd.qcut(temp[feat], q=8, duplicates='drop')
    else:
        temp['bin'] = pd.cut(temp[feat], bins=5)
    churn_rate = temp.groupby('bin', observed=False)['is_active'].apply(
        lambda x: (1 - x.mean()) * 100).reset_index(name='churn_rate')
    ax.bar(range(len(churn_rate)), churn_rate['churn_rate'].values,
           color=['#2ecc71' if v < churn_rate['churn_rate'].mean() else '#e74c3c'
                  for v in churn_rate['churn_rate'].values], alpha=0.85)
    ax.set_xticks(range(len(churn_rate)))
    ax.set_xticklabels([str(b)[:15] for b in churn_rate['bin']], rotation=30, ha='right', fontsize=6)
    ax.set_title(f'流失率 vs {label}', fontsize=12, fontweight='bold')
    ax.set_ylabel('流失率 (%)'), ax.grid(axis='y', alpha=0.3)
    ax.axhline(y=14.8, color='red', linestyle='--', alpha=0.5, label='平均流失率')
    ax.legend(fontsize=7)

plt.tight_layout()
plt.savefig('churn_by_features.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] churn_by_features.png")

# --- 预测概率分布 ---
fig, axes = plt.subplots(2, 4, figsize=(18, 10))
axes = axes.flatten()
for idx, (name, r) in enumerate(results.items()):
    if idx >= 8:
        break
    ax = axes[idx]
    ax.hist(r['y_prob'][y_test == 0], bins=40, alpha=0.6, label='实际流失', color='#e74c3c', density=True)
    ax.hist(r['y_prob'][y_test == 1], bins=40, alpha=0.6, label='实际未流失', color='#2ecc71', density=True)
    ax.axvline(x=r['best_threshold'], color='black', linestyle='--', label=f'阈值={r["best_threshold"]:.2f}')
    ax.set_title(name, fontsize=11, fontweight='bold')
    ax.legend(fontsize=7)

# 隐藏多余的子图
for idx in range(len(results), 8):
    axes[idx].set_visible(False)

plt.suptitle('各模型预测概率分布', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('probability_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  [OK] probability_distribution.png")

# ============================================================
# 最终总结
# ============================================================
print("\n" + "=" * 60)
print("实验完成！")
print(f"最佳模型: {best_model}")
print(f"最佳F1分数: {results_df.iloc[0]['F1分数']:.4f}")
print(f"最佳AUC: {results_df.sort_values('AUC', ascending=False).iloc[0]['AUC']:.4f}")
print("\n生成文件列表:")
import os
for f in os.listdir('.'):
    if f.endswith('.png'):
        print(f"  - {f}")
print("=" * 60)
