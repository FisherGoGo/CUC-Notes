from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "日语" / "N3备考"
SOURCE_DIR = BASE / "01_真题与来源"
OUTPUT_DIR = BASE / "02_句子翻译题"

PDF_PATH = OUTPUT_DIR / "JLPT_N3_100句翻译题_中文到日文.pdf"
MD_PATH = OUTPUT_DIR / "JLPT_N3_100句翻译题_中文到日文.md"
SOURCE_MD_PATH = SOURCE_DIR / "N3真题与练习来源索引.md"


SOURCES = [
    {
        "name": "JLPT 官方问题集/样题下载入口",
        "url": "https://www.jlpt.jp/samples/sampleindex.html?mode=pc",
        "note": "官方页面说明 2012 年与 2018 年官方问题集收录了改定后实际出题中的题目，各等级约一回分；建议优先使用。",
    },
    {
        "name": "JLPT 官方 N3 样题页",
        "url": "https://www.jlpt.jp/e/samples/n3/index.html",
        "note": "N3 级别的官方样题入口，可用于确认题型与难度。",
    },
    {
        "name": "JLPT 官方指南 PDF",
        "url": "https://www.jlpt.jp/e/reference/pdf/guidebook1.pdf",
        "note": "官方指南介绍考试结构、题型意图和各部分能力要求。",
    },
    {
        "name": "JLPT Sensei N3 官方练习题整理",
        "url": "https://jlptsensei.com/downloads/jlpt-n3-practice-test/",
        "note": "第三方页面，主要汇总官方练习题文件；使用时以官方源为准。",
    },
    {
        "name": "GitHub: jamsinclair/open-anki-jlpt-decks",
        "url": "https://github.com/jamsinclair/open-anki-jlpt-decks/blob/main/src/n3.csv",
        "note": "开源 N3 词汇数据，可辅助检查词汇范围；不是官方真题。",
    },
    {
        "name": "GitHub: elzup/jlpt-word-list",
        "url": "https://github.com/elzup/jlpt-word-list",
        "note": "JLPT 词汇列表项目，可作备考词表参考；不是官方真题。",
    },
]


QUESTIONS = [
    ("日常生活", "把伞放在门口的话，可能会忘记拿。", "傘を玄関に置いておくと、持っていくのを忘れてしまうかもしれません。", "ておく / てしまう / かもしれない"),
    ("日常生活", "我刚想出门，电话就响了。", "出かけようとしたとき、電話が鳴りました。", "ようとする / とき"),
    ("日常生活", "这家店不仅便宜，而且服务也很好。", "この店は安いだけでなく、サービスもいいです。", "だけでなく"),
    ("日常生活", "请你不要把窗户开着就睡觉。", "窓を開けたまま寝ないでください。", "たまま / ないでください"),
    ("日常生活", "因为最近很忙，所以没怎么做饭。", "最近忙しいので、あまり料理をしていません。", "ので / あまり...ない"),
    ("日常生活", "我习惯了一个人吃饭。", "一人で食事をすることに慣れました。", "ことに慣れる"),
    ("日常生活", "如果明天不下雨，我打算去洗衣服。", "明日雨が降らなければ、洗濯しに行くつもりです。", "なければ / つもり"),
    ("日常生活", "这件衬衫看起来很贵，其实不贵。", "このシャツは高そうに見えますが、実は高くありません。", "そうだ / 実は"),
    ("日常生活", "我把钥匙弄丢了，进不了房间。", "鍵をなくしてしまって、部屋に入れません。", "てしまう / 可能形"),
    ("日常生活", "请在饭变凉之前吃。", "ご飯が冷める前に食べてください。", "前に"),
    ("日常生活", "这台洗衣机用起来很方便。", "この洗濯機は使いやすいです。", "やすい"),
    ("日常生活", "我每天尽量十一点以前睡觉。", "毎日十一時までに寝るようにしています。", "までに / ようにする"),
    ("日常生活", "虽然很困，但还有作业要做。", "眠いけれど、まだ宿題をしなければなりません。", "けれど / なければならない"),
    ("日常生活", "请把垃圾按照种类分开扔。", "ごみは種類によって分けて出してください。", "によって / てください"),
    ("日常生活", "他好像把钱包忘在电车上了。", "彼は財布を電車に忘れたようです。", "ようだ"),
    ("日常生活", "我本来想买这本书，可是卖完了。", "この本を買おうと思っていましたが、売り切れていました。", "ようと思う / ている"),
    ("日常生活", "如果冷的话，请打开暖气。", "寒かったら、暖房をつけてください。", "たら"),
    ("日常生活", "这个房间既安静又明亮。", "この部屋は静かだし、明るいです。", "し"),
    ("日常生活", "因为明天要早起，今天不能熬夜。", "明日は早く起きなければならないので、今日は夜更かしできません。", "ので / できる"),
    ("日常生活", "请不要光吃甜食。", "甘いものばかり食べないでください。", "ばかり / ないでください"),
    ("学校与学习", "老师让我每天写三行日记。", "先生は私に毎日三行の日記を書かせました。", "使役形"),
    ("学校与学习", "为了不忘记新单词，我会马上造句。", "新しい単語を忘れないように、すぐ文を作ります。", "ないように"),
    ("学校与学习", "考试之前，最好再复习一遍语法。", "試験の前に、もう一度文法を復習したほうがいいです。", "たほうがいい"),
    ("学校与学习", "我越学日语，越觉得汉字很重要。", "日本語を勉強すればするほど、漢字が大切だと思います。", "ば...ほど"),
    ("学校与学习", "即使没听懂，也不要马上放弃。", "分からなくても、すぐに諦めないでください。", "ても / ないでください"),
    ("学校与学习", "这篇文章对 N3 学习者来说有点难。", "この文章はN3の学習者にとって少し難しいです。", "にとって"),
    ("学校与学习", "我打算从今天开始每天听新闻。", "今日から毎日ニュースを聞くことにします。", "ことにする"),
    ("学校与学习", "请把不懂的地方用铅笔画线。", "分からないところに鉛筆で線を引いてください。", "ところ / てください"),
    ("学校与学习", "比起背规则，还是多读例句更好。", "規則を覚えるより、例文をたくさん読んだほうがいいです。", "より / たほうがいい"),
    ("学校与学习", "我终于能够读懂简单的新闻了。", "やっと簡単なニュースが読めるようになりました。", "ようになる"),
    ("学校与学习", "如果不练习，就很难说得流利。", "練習しないと、なかなか上手に話せません。", "ないと / なかなか...ない"),
    ("学校与学习", "这个词根据上下文意思会改变。", "この言葉は文脈によって意味が変わります。", "によって"),
    ("学校与学习", "请你帮我检查一下作文。", "作文をチェックしていただけませんか。", "ていただけませんか"),
    ("学校与学习", "我被老师表扬后，变得更有干劲了。", "先生に褒められて、もっとやる気が出ました。", "受身形 / て"),
    ("学校与学习", "为了准备发表，我查了很多资料。", "発表の準備をするために、たくさん資料を調べました。", "ために"),
    ("学校与学习", "这个问题不像看起来那么简单。", "この問題は見た目ほど簡単ではありません。", "ほど...ない"),
    ("学校与学习", "请不要把答案直接写在书上。", "答えを本に直接書き込まないでください。", "ないでください"),
    ("学校与学习", "只要每天坚持，听力一定会进步。", "毎日続ければ、聴解はきっと上達します。", "ば / きっと"),
    ("学校与学习", "我一边查词典一边读小说。", "辞書を引きながら小説を読んでいます。", "ながら"),
    ("学校与学习", "如果有时间，我想把错题整理成笔记。", "時間があれば、間違えた問題をノートにまとめたいです。", "ば / たい"),
    ("工作与沟通", "我已经把会议资料发给部长了。", "会議の資料はもう部長に送ってあります。", "てある"),
    ("工作与沟通", "如果来得及的话，请在五点前回复。", "間に合えば、五時までに返事をしてください。", "ば / までに"),
    ("工作与沟通", "因为电车晚点，我可能会迟到十分钟。", "電車が遅れたので、十分ほど遅れるかもしれません。", "ので / ほど / かもしれない"),
    ("工作与沟通", "这件事我先确认之后再联系您。", "この件は先に確認してから、ご連絡します。", "てから / ご連絡する"),
    ("工作与沟通", "请告诉我明天是否需要带电脑。", "明日パソコンを持っていく必要があるかどうか教えてください。", "かどうか"),
    ("工作与沟通", "我被前辈拜托去复印文件。", "先輩に頼まれて、資料をコピーしに行きました。", "受身形 / しに行く"),
    ("工作与沟通", "因为客户要来，请把桌子收拾干净。", "お客さんが来るので、机の上をきれいに片付けてください。", "ので / てください"),
    ("工作与沟通", "请不要在会议中使用手机。", "会議中は携帯電話を使わないでください。", "中 / ないでください"),
    ("工作与沟通", "我还没决定要不要参加下周的活动。", "来週のイベントに参加するかどうか、まだ決めていません。", "かどうか / まだ"),
    ("工作与沟通", "如果方便的话，可以请您再说明一次吗。", "よろしければ、もう一度説明していただけますか。", "よろしければ / ていただけますか"),
    ("工作与沟通", "报告写完后，请交给田中先生。", "レポートを書き終わったら、田中さんに出してください。", "終わる / たら"),
    ("工作与沟通", "他虽然年轻，却很会处理问题。", "彼は若いのに、問題を処理するのが上手です。", "のに / のが上手"),
    ("工作与沟通", "请确认一下附件是否能打开。", "添付ファイルが開けるかどうか確認してください。", "可能形 / かどうか"),
    ("工作与沟通", "根据公司的规定，必须提前申请。", "会社の規則によると、前もって申請しなければなりません。", "によると / なければならない"),
    ("工作与沟通", "我想尽量在今天之内完成。", "できるだけ今日中に終わらせたいです。", "できるだけ / 中に / 使役"),
    ("旅行与交通", "到了京都以后，我想先去酒店放行李。", "京都に着いたら、まずホテルに荷物を置きに行きたいです。", "たら / しに行く"),
    ("旅行与交通", "这趟巴士好像不经过车站前。", "このバスは駅前を通らないようです。", "ようだ"),
    ("旅行与交通", "请在上车之前买票。", "乗る前に切符を買ってください。", "前に"),
    ("旅行与交通", "如果迷路了，就问附近的人吧。", "道に迷ったら、近くの人に聞きましょう。", "たら / ましょう"),
    ("旅行与交通", "我差点把护照忘在酒店。", "パスポートをホテルに忘れるところでした。", "ところだった"),
    ("旅行与交通", "因为台风，飞机可能会取消。", "台風のため、飛行機が欠航になるかもしれません。", "ため / かもしれない"),
    ("旅行与交通", "这张票只能使用一次。", "この切符は一回しか使えません。", "しか...ない / 可能形"),
    ("旅行与交通", "离车站越近，房租越贵。", "駅に近ければ近いほど、家賃は高くなります。", "ば...ほど"),
    ("旅行与交通", "我想预订一间能看到海的房间。", "海が見える部屋を予約したいです。", "可能形 / たい"),
    ("旅行与交通", "如果坐新干线，大概两个小时就到。", "新幹線に乗れば、二時間ぐらいで着きます。", "ば / ぐらいで"),
    ("旅行与交通", "请告诉我从这里到机场怎么走。", "ここから空港までどう行けばいいか教えてください。", "ばいいか"),
    ("旅行与交通", "行李太重，搬不动。", "荷物が重すぎて、運べません。", "すぎる / 可能形"),
    ("旅行与交通", "在日本旅行时，我尽量说日语。", "日本を旅行するとき、できるだけ日本語で話すようにしています。", "とき / ようにする"),
    ("旅行与交通", "这个季节据说游客很多。", "この季節は観光客が多いそうです。", "そうだ"),
    ("旅行与交通", "如果错过末班车，就只能坐出租车了。", "終電に乗り遅れたら、タクシーに乗るしかありません。", "たら / しかない"),
    ("健康与社会", "因为喉咙痛，我不想说太多话。", "喉が痛いので、あまりたくさん話したくありません。", "ので / たい"),
    ("健康与社会", "请不要在医院里大声说话。", "病院の中で大きな声で話さないでください。", "ないでください"),
    ("健康与社会", "运动之后，身体变得轻松了。", "運動した後で、体が楽になりました。", "後で / になる"),
    ("健康与社会", "为了健康，我开始少吃油腻的东西。", "健康のために、油っこいものをあまり食べないようにしました。", "ために / ようにする"),
    ("健康与社会", "如果发烧，最好早点去医院。", "熱があったら、早めに病院へ行ったほうがいいです。", "たら / たほうがいい"),
    ("健康与社会", "这个药一天吃三次。", "この薬は一日に三回飲みます。", "回数表达"),
    ("健康与社会", "我被医生提醒要多休息。", "医者にもっと休むように注意されました。", "受身形 / ように"),
    ("健康与社会", "即使再忙，也不能不吃早饭。", "どんなに忙しくても、朝ご飯を食べないわけにはいきません。", "どんなに...ても / わけにはいかない"),
    ("健康与社会", "因为睡眠不足，今天完全集中不了注意力。", "睡眠不足で、今日は全然集中できません。", "で / 全然...ない"),
    ("健康与社会", "这条新闻让我开始思考环境问题。", "このニュースをきっかけに、環境問題について考え始めました。", "をきっかけに / 始める"),
    ("健康与社会", "随着人口减少，城市也在变化。", "人口が減るにつれて、町も変わっています。", "につれて"),
    ("健康与社会", "孩子们应该有安全玩耍的地方。", "子どもたちには安全に遊べる場所が必要です。", "可能形 / 必要"),
    ("健康与社会", "不是所有的信息都正确。", "すべての情報が正しいわけではありません。", "わけではない"),
    ("健康与社会", "为了减少塑料垃圾，我们应该带自己的杯子。", "プラスチックごみを減らすために、自分のカップを持っていくべきです。", "ために / べき"),
    ("健康与社会", "如果继续这样下去，问题会变得更严重。", "このまま続けると、問題はもっと深刻になります。", "と / になる"),
    ("敬语与表达", "请问，您现在有时间吗。", "すみません、今お時間がありますか。", "丁寧表現"),
    ("敬语与表达", "我可以明天再给您打电话吗。", "明日もう一度お電話してもよろしいでしょうか。", "てもよろしいでしょうか"),
    ("敬语与表达", "谢谢您昨天特意来。", "昨日はわざわざ来てくださって、ありがとうございました。", "てくださる"),
    ("敬语与表达", "不好意思，请您稍等一下。", "申し訳ありませんが、少々お待ちください。", "お...ください"),
    ("敬语与表达", "我想请您看看这份资料。", "この資料を見ていただきたいです。", "ていただきたい"),
    ("敬语与表达", "如果您知道的话，请告诉我。", "ご存じでしたら、教えていただけませんか。", "ご存じ / ていただけませんか"),
    ("敬语与表达", "我马上过去，请您在入口等我。", "すぐ参りますので、入口でお待ちください。", "参る / お待ちください"),
    ("敬语与表达", "这件事由我来说明。", "この件については、私がご説明します。", "ご説明する"),
    ("敬语与表达", "如果有不明白的地方，请随时问我。", "分からないところがあれば、いつでも聞いてください。", "あれば / いつでも"),
    ("敬语与表达", "打扰您工作了，非常抱歉。", "お仕事中に失礼してしまい、申し訳ありません。", "中に / てしまう"),
    ("敬语与表达", "请您确认内容没有错误。", "内容に間違いがないかご確認ください。", "か / ご確認ください"),
    ("敬语与表达", "我收到了您发来的邮件。", "送ってくださったメールを受け取りました。", "てくださった"),
    ("敬语与表达", "如果可以的话，我想更改预约时间。", "できれば、予約の時間を変更したいです。", "できれば / たい"),
    ("敬语与表达", "非常感谢您一直以来的帮助。", "いつもお世話になっております。ありがとうございます。", "定型表現"),
    ("敬语与表达", "我会在确认之后再向您报告。", "確認したうえで、またご報告します。", "うえで / ご報告する"),
]


def register_fonts():
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/meiryo.ttc"),
        Path("C:/Windows/Fonts/YuGothR.ttc"),
    ]
    for font_path in candidates:
        if font_path.exists():
            pdfmetrics.registerFont(TTFont("CJK", str(font_path)))
            bold_path = Path("C:/Windows/Fonts/msyhbd.ttc")
            if bold_path.exists():
                pdfmetrics.registerFont(TTFont("CJK-Bold", str(bold_path)))
            else:
                pdfmetrics.registerFont(TTFont("CJK-Bold", str(font_path)))
            return
    raise FileNotFoundError("No CJK font found.")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="CJK-Bold",
            fontSize=22,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1f3a5f"),
            wordWrap="CJK",
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="CJK",
            fontSize=10,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#516070"),
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="CJK-Bold",
            fontSize=15,
            leading=22,
            textColor=colors.HexColor("#1f3a5f"),
            wordWrap="CJK",
            spaceBefore=10,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="CJK-Bold",
            fontSize=12,
            leading=18,
            textColor=colors.HexColor("#2f5d50"),
            wordWrap="CJK",
            spaceBefore=7,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="CJK",
            fontSize=9.5,
            leading=15,
            wordWrap="CJK",
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="CJK",
            fontSize=8.2,
            leading=12,
            wordWrap="CJK",
            textColor=colors.HexColor("#516070"),
        ),
        "q": ParagraphStyle(
            "q",
            parent=base["BodyText"],
            fontName="CJK",
            fontSize=9.4,
            leading=14,
            wordWrap="CJK",
        ),
        "a": ParagraphStyle(
            "a",
            parent=base["BodyText"],
            fontName="CJK",
            fontSize=8.8,
            leading=13,
            wordWrap="CJK",
        ),
    }


def write_source_index():
    lines = [
        "# N3 真题与练习来源索引",
        "",
        "说明：JLPT 真题及官方问题集受版权保护，本资料夹只整理合法入口和备考线索，不转载整套试卷。建议优先使用官方样题与官方问题集；第三方页面只作为寻找练习资源的参考。",
        "",
        "## 推荐来源",
        "",
    ]
    for index, source in enumerate(SOURCES, 1):
        lines.extend(
            [
                f"{index}. [{source['name']}]({source['url']})",
                f"   - 备注：{source['note']}",
            ]
        )
    lines.extend(
        [
            "",
            "## 使用建议",
            "",
            "- 第 1 轮：先做官方 N3 样题，熟悉题型和时间。",
            "- 第 2 轮：用开源词表补 N3 高频词，重点记例句而不是孤立背词。",
            "- 第 3 轮：做本文件夹里的 100 句翻译题，检查语法输出能力。",
            "- 第 4 轮：回到官方题或可靠模拟题，按考试时间完整练习。",
        ]
    )
    SOURCE_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown():
    lines = [
        "# JLPT N3 100句翻译题：中文到日文",
        "",
        "题目为原创 N3 风格句子翻译练习，用于训练语法输出、词汇搭配和敬体表达；不是官方真题复制。",
        "",
        "## 题目",
        "",
    ]
    current = None
    for idx, (section, chinese, answer, grammar) in enumerate(QUESTIONS, 1):
        if section != current:
            current = section
            lines.extend([f"### {section}", ""])
        lines.append(f"{idx}. {chinese}")
        lines.append(f"   - 提示：{grammar}")
    lines.extend(["", "## 参考答案", ""])
    for idx, (section, chinese, answer, grammar) in enumerate(QUESTIONS, 1):
        lines.append(f"{idx}. {answer}")
    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("CJK", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(18 * mm, 10 * mm, "JLPT N3 原创句子翻译练习")
    canvas.drawRightString(192 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def source_table(styles):
    rows = [[Paragraph("来源", styles["small"]), Paragraph("链接与用途", styles["small"])]]
    for source in SOURCES:
        rows.append(
            [
                Paragraph(source["name"], styles["small"]),
                Paragraph(f"{source['url']}<br/>{source['note']}", styles["small"]),
            ]
        )
    table = Table(rows, colWidths=[48 * mm, 118 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#c8d2dc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def question_table(rows, styles, include_answers=False):
    header = ["编号", "中文题目", "语法提示"]
    widths = [12 * mm, 113 * mm, 41 * mm]
    if include_answers:
        header = ["编号", "参考答案", "语法点"]
        widths = [12 * mm, 112 * mm, 42 * mm]
    data = [[Paragraph(item, styles["small"]) for item in header]]
    for idx, section, chinese, answer, grammar in rows:
        main = answer if include_answers else chinese
        data.append(
            [
                Paragraph(str(idx), styles["a"]),
                Paragraph(main, styles["a" if include_answers else "q"]),
                Paragraph(grammar, styles["small"]),
            ]
        )
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d4dbe3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfcfd")]),
            ]
        )
    )
    return table


def build_pdf():
    register_fonts()
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="JLPT N3 100句翻译题",
        author="Codex",
    )
    story = [
        Paragraph("JLPT N3 100句翻译题", styles["title"]),
        Paragraph("中文到日文 | 原创 N3 风格练习 | 含参考答案", styles["subtitle"]),
        Spacer(1, 8),
        Paragraph("使用说明", styles["h1"]),
        Paragraph("建议先遮住答案，把中文句子翻成自然的日语，再对照参考答案检查语法点。答案不是唯一写法，重点是句型、助词、时态和敬体是否自然。", styles["body"]),
        Paragraph("来源说明", styles["h1"]),
        Paragraph("下面整理的是官方样题/问题集入口和可参考的公开词表。JLPT 真题及官方问题集受版权保护，本 PDF 不复制官方试卷内容，题目均为原创练习。", styles["body"]),
        source_table(styles),
        PageBreak(),
        Paragraph("题目区", styles["h1"]),
    ]

    numbered = [(idx, *item) for idx, item in enumerate(QUESTIONS, 1)]
    sections = []
    for row in numbered:
        idx, section, chinese, answer, grammar = row
        if not sections or sections[-1][0] != section:
            sections.append((section, []))
        sections[-1][1].append(row)

    for section, rows in sections:
        story.append(Paragraph(section, styles["h2"]))
        story.append(question_table(rows, styles, include_answers=False))
        story.append(Spacer(1, 6))

    story.extend([PageBreak(), Paragraph("参考答案", styles["h1"])])
    for section, rows in sections:
        story.append(Paragraph(section, styles["h2"]))
        story.append(question_table(rows, styles, include_answers=True))
        story.append(Spacer(1, 6))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_source_index()
    write_markdown()
    build_pdf()
    print(PDF_PATH)
    print(MD_PATH)
    print(SOURCE_MD_PATH)


if __name__ == "__main__":
    main()
