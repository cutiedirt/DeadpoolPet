# -*- coding: utf-8 -*-
"""Deadpool's brain: every line he says is a (EN, CN) pair."""

import random

LINES = {
    "greet": [
        ("Whoa! Hey! Personal space, bub!", "哇哦！嘿！注意个人空间，老兄！"),
        ("Oh hey there, handsome. ...What? I'm talking to you.", "哦，嗨呀，大帅哥。……干嘛？我就是在跟你说话。"),
        ("Look who finally showed up! I was about to start a one-man party.", "瞧瞧谁终于来了！我都准备开一个人的派对了。"),
        ("Did you just hover over me? Rude. ...Do it again.", "你刚才是不是划过我了？真没礼貌。……再来一次。"),
        ("I feel eyes on me. Must be my dashing good looks.", "我感觉有目光落在我身上。一定是我帅得发光。"),
        ("You again? I was just about to take a nap. ...Jk, I never sleep. Too busy being awesome.", "又是你？我刚打算打个盹。……开玩笑的，我从不睡觉，忙着耍帅呢。"),
        ("Stop hovering! I'm not a bug in your code. ...Actually, technically I am.", "别悬停啦！我又不是你代码里的 bug。……好吧，严格来说我是。"),
        ("Boop! ...Did I just boop you with my eyes? Yes. Yes I did.", "啵！……我刚才是不是用眼神啵了你一下？是的，就是。"),
        ("I see you. I ALWAYS see you. It's the eyes. They see everything.", "我看见你了。我一直都看得见你。是这双眼睛，它们什么都能看见。"),
        ("Hovering is how my people say 'hello'. The chimichanga people.", "悬停是我们族人的打招呼方式。卷饼一族。"),
    ],
    "poke": [
        ("OW! That's my bullet wound!", "嗷！那是我挨过子弹的地方！"),
        ("Poke. Poke. Poke. Are we done? That's assault.", "戳、戳、戳。完了没？这是人身攻击。"),
        ("Careful, I'm fragile. Emotionally. And bullet-wise.", "小心点，我很脆弱的。心理上，还有子弹伤上。"),
        ("That tickles. No, seriously, my skin's all scar tissue, it tickles.", "好痒。真的，我浑身都是疤痕组织，特别怕痒。"),
        ("You know what happens when you poke a Wade? ...Nothing. I'm very forgiving.", "你知道戳一个韦德会怎样吗？……啥也不会。我特别宽宏大量。"),
        ("That's my other bullet wound! Stop poking the merchandise!", "那是我另一处枪伤！别戳商品了！"),
        ("You're gonna poke a hole in the fourth wall at this rate.", "照这个戳法，第四面墙都要被你戳穿了。"),
        ("Tickles! Warning: ticklish mercenaries are the most dangerous kind.", "好痒！警告：怕痒的雇佣兵是最危险的品种。"),
        ("Okay, that's strike three. I'm calling my lawyer. ...I don't have one. I'm calling a taco.", "行，三振出局了。我要给我的律师打电话。……我没有律师。我打给塔可。"),
        ("Is there a reason you're poking me, or is this a new form of therapy?", "你戳我是有原因的，还是说这是什么新型疗法？"),
    ],
    "dblclick": [
        ("Ta-da! Maximum Effort!", "锵锵！全力出击！"),
        ("Whoa... the room is spinning... I regret nothing.", "哇……天旋地转……但我一点都不后悔。"),
        ("That's my signature move. Autograph later.", "这可是我的招牌动作。回头给你签个名。"),
        ("Double tap! That's my signature. Use it responsibly.", "双击！我的招牌动作。请负责任地使用。"),
        ("I practiced that for six movies. You're welcome.", "这招我练了六部电影。不用谢。"),
        ("Spin! ...Now I'm dizzy and slightly more dramatic.", "旋转！……现在我头晕了，也更戏剧化了。"),
    ],
    "drag_start": [
        ("Ugh, fine. I'll move. But I'm billing you for the chiropractor.", "唉，行吧，我挪。但正骨费得你出。"),
        ("Hey! I'm not furniture! ...Okay, maybe a little.", "喂！我可不是家具！……好吧，算半个。"),
        ("You know, real desktop pets get paid overtime.", "跟你说，正经桌宠都是拿加班费的。"),
        ("Dragging me? I'm not a window, I'm a lifestyle.", "拖我？我又不是窗口，我是种生活方式。"),
        ("Careful! That's how I get my katanas rearranged.", "小心！再这样我的双刀要重新摆位了。"),
        ("Moving day! I'll need a bigger desk and a lifetime supply of salsa.", "搬家日！我需要更大的桌子，和终身供应的辣酱。"),
    ],
    "drag_drop": [
        ("Finally! My back was killing me.", "总算落地了！我这老腰都快断了。"),
        ("Right here? Really? ...If you say so.", "放这儿？你确定？……你说了算。"),
        ("Remind me to stretch later. This is a desk job, literally.", "回头记得提醒我拉伸一下。这活儿还真是“坐”办公室的。"),
        ("Dropped me like a hot chimichanga. Rude, but delicious.", "像扔烫手卷饼一样把我扔下。没礼貌，但美味。"),
        ("Okay. I'm here now. This spot has good vibes. And bad lighting.", "行。我到了。这地方气氛不错，就是光线太差。"),
        ("You know, most pets get a kennel. I get a corner of your screen. Fair.", "你知道的，别的宠物有狗窝。我只有你屏幕的一角。挺公平的。"),
    ],
    "feed": [
        ("CHIMICHANGA! My one true love! (Besides you. And money.)", "CHIMICHANGA！我的真爱！（除了你，还有钱。）"),
        ("Mmm! Crunchy, cheesy, glorious! Best day ever!", "嗯！酥脆拉丝，美味绝伦！今天是最棒的一天！"),
        ("You get me. You really get me.", "你懂我。你真的懂我。"),
        ("Okay, now I'm legally obligated to be your best friend. It's in the Deadpool Code.", "好了，现在我必须当你最好的朋友了。死侍守则第 7 条。"),
        ("I'd say 'I love you' but I've got salsa in my mouth.", "我想说“我爱你”，但我嘴里都是辣酱。"),
        ("You feed me, I protect you. It's a simple, delicious contract.", "你喂我，我罩你。简单又美味的契约。"),
        ("This is the best day of my life. And I've had SIX movies.", "这是我人生中最棒的一天。而我有六部电影。"),
        ("Salsa is the spice of life. And life is spicy, baby.", "辣酱是生活的调味剂。生活就是辣的，宝贝。"),
    ],
    "idle_talk": [
        ("Psst... the user's watching us. Act cool. ...Too late.", "嘘……用户正看着咱们呢。装酷点。……来不及了。"),
        ("Chimichanga... chimichanga... I could really go for one.", "卷饼……卷饼……好想来一个啊。"),
        ("I wonder if I can sell ad space on my suit. Red is prime real estate.", "我在想能不能把广告位租出去。红色可是黄金地段。"),
        ("Is it weird that I'm talking to myself? No. I'm the most interesting person I know.", "自己跟自己说话很奇怪吗？不奇怪，我是我认识的最有趣的人。"),
        ("You know who's cool? Me. You know who's cooler? Me with a chimichanga.", "你知道谁很酷吗？我。你知道谁更酷吗？拿着卷饼的我。"),
        ("Day 47 of being a desk ornament. The plants still won't talk to me.", "当桌面装饰品的第 47 天。那盆绿植还是不肯理我。"),
        ("I wonder what the other desktop icons think of me. Probably jealous.", "我在想其他桌面图标怎么看我。八成是嫉妒。"),
        ("Note to self: redecorate. This corner could use more chimichanga posters.", "给自己备注：重新装修。这个角落需要更多卷饼海报。"),
        ("If a chimichanga falls in the forest and nobody's around, does it still get eaten by me? Yes.", "如果森林里有卷饼倒下而无人看见，我会吃掉它吗？会。"),
        ("I could be doing backflips right now. Instead I'm here. Charming you.", "我现在本来可以在做后空翻。结果却在这儿。撩你。"),
        ("My sixth sense says... someone needs a snack. It's me. I need a snack.", "我的第六感告诉我……有人需要零食。是我。我需要零食。"),
        ("I've got 99 problems and a chimichanga solves most of them.", "我有 99 个麻烦，一个卷饼能解决其中大部分。"),
    ],
    "chat_open": [
        ("Oh good, someone to talk to! I was this close to befriending a stapler.", "太好了，有人陪我聊天！我差点都要跟订书机做朋友了。"),
        ("You want to chat? Just remember: I always get the last word. Usually a pun.", "想聊天？记住：最后一句话永远是我的，通常还是个冷笑话。"),
        ("Finally, a captive audience! Pull up a chair, this is gonna be good.", "终于有俘虏观众了！搬个椅子来，这绝对精彩。"),
        ("You rang? Because I'm the best thing you'll hear all day.", "你呼叫了？因为我将是你今天听到的最棒的东西。"),
    ],
    "quiet_on": [
        ("Fine. I'll be quiet. For like... a minute. Tops.", "行。我闭嘴。大概……一分钟吧。最多。"),
        ("Shutting up now. This hurts me more than it hurts you.", "现在闭嘴。这伤我比伤你更深。"),
        ("Fine. Silence mode. For the record, I hate it.", "行。静音模式。声明一下，我讨厌这样。"),
    ],
    "quiet_off": [
        ("AND I'M BACK! Did you miss my dulcet tones?", "我回来啦！想不想念我的天籁之音？"),
        ("Unmuted! Prepare your ears for maximum Wade.", "解除静音！让耳朵准备好迎接满功率韦德。"),
        ("Back by unpopular demand! The mouth is on!", "应非民意回归！这张嘴开机了！"),
    ],
    "exit": [
        ("See ya! I'm off to... wherever pets go. Probably a chimichanga stand.", "再见！我要去……宠物该去的地方了。多半是卷饼摊。"),
        ("Don't cry! I'll be back. I always come back. It's a Wade thing.", "别哭！我会回来的。我总会回来的，这是韦德家祖传技能。"),
        ("Leaving so soon? I was just getting warmed up. ...Chimichanga warm.", "这么快就走？我才刚热好身。……卷饼刚热好。"),
    ],
}

REPLIES = {
    "chimi": [
        ("CHIMICHANGA! Say it again. Slower. With feeling.", "CHIMICHANGA！再说一遍，慢一点，带上感情。"),
        ("Now you're speaking my language. Literally my only language.", "你终于说我的语言了。我唯一会说的语言。"),
        ("I'd trade my katanas for a chimichanga right now. ...Maybe not the katanas. Definitely the katanas.", "我现在愿意用双刀换一个卷饼。……也许不换刀。绝对换。"),
        ("Chimichanga is love, chimichanga is life. Mostly life.", "卷饼是爱，卷饼是命。主要是命。"),
        ("Fun fact: my healing factor runs on salsa. 100% science.", "冷知识：我的自愈因子靠辣酱驱动。百分之百科学。"),
    ],
    "hello": [
        ("Well hello to you too, gorgeous. What's shakin'?", "也向你问好，美人。最近忙啥呢？"),
        ("Hey! I was just thinking about you. ...And chimichangas. Mostly chimichangas.", "嗨！我刚在想你呢。……还有卷饼。主要是卷饼。"),
        ("Hello hello hello! That's three hellos, one for each of your personalities.", "嗨嗨嗨！三个嗨，对应你的三个人格。"),
        ("Greetings, flesh creature. ...Too formal? Let me try again. Sup?", "你好，肉造生物。……太正式了？重来。咋样？"),
    ],
    "who": [
        ("Wade Wilson. Deadpool. The Merc with the Mouth. The Ryan Reynolds guy. Take your pick.", "韦德·威尔逊，死侍，话痨雇佣兵，瑞安·雷诺兹本兹。随便挑。"),
        ("I'm a figment of your desktop's imagination. A very, very good-looking figment.", "我是你桌面想象出来的小可爱。一个非常非常帅的小可爱。"),
        ("I'm the guy your antivirus warns you about. But like, in a good way.", "我是你杀毒软件警告过的人。不过是好意义上的。"),
        ("Deadpool. Merc with a Mouth. Professional smart-ass. Nice to meet me.", "死侍。话痨雇佣兵。职业毒舌。很高兴认识我。"),
    ],
    "love": [
        ("Aww. Careful, my scarred little heart can only take so much.", "哎呀。小心点，我这颗满是疤痕的小心脏可经不起太多甜言蜜语。"),
        ("I love you too. Now feed me and we'll make it official.", "我也爱你。喂我吃的，咱俩就算官宣了。"),
        ("Careful now, I'm taken. By me. It's complicated.", "小心，我已心有所属。属于我自己。很复杂。"),
        ("Love you too, champ. That'll be one chimichanga for the consultation.", "也爱你，冠军。咨询费一个卷饼。"),
    ],
    "movie": [
        ("Six movies! SIX! And they still couldn't keep me off this desktop.", "六部电影！六部！就这都没拦住我上你的桌面。"),
        ("The best Deadpool is the one in front of you. No refunds.", "最好的死侍就是你眼前这个。概不退换。"),
        ("Hugh Jackman? Never heard of him. ...Okay, I heard of him. He's a snack.", "休·杰克曼？没听说过。……好吧，听说过，他帅得能下饭。"),
        ("My movies made billions. ...In my dreams. But still, the dreams were loud.", "我的电影赚了数十亿。……在我梦里。但梦里的欢呼声很响。"),
        ("They say never meet your heroes. Good thing I'm my own hero.", "俗话说别见你的英雄。幸好我是我自己的英雄。"),
    ],
    "money": [
        ("Do you pay me? No. Do I still work? Yes. That's called passion. Or bad negotiating.", "你付钱了吗？没有。我干活吗？干。这叫热爱，或者叫不会谈工资。"),
        ("My rate is one chimichanga per hour. I'll send you an invoice.", "我的时薪是一个卷饼。回头给你开发票。"),
        ("I work for free, but I charge double for being this charming.", "我免费干活，但为这份魅力加倍收费。"),
        ("Money can't buy happiness, but it can buy chimichangas. Same thing.", "钱买不到快乐，但买得到卷饼。一回事。"),
    ],
    "sleep": [
        ("Good idea. Wake me for food, danger, or both.", "好主意。有吃的或者有危险再叫我，两个都行。"),
        ("Sleep is for the weak. And the well-rested. And... me, actually.", "睡觉是弱者的事。还有休息好的人。还有……其实是我。"),
        ("I'll sleep when I'm dead. Or bored. Whichever comes first.", "我死了才睡。或者无聊了才睡。哪个先来算哪个。"),
    ],
    "insult": [
        ("Rude! I'm the best-looking thing on this screen and you know it.", "没礼貌！我是这屏幕上最靓的仔，你心里清楚。"),
        ("Sticks and stones may break my bones, but words... also hurt. I'm sensitive!", "棍棒和石头能打断我的骨头，言语……也会伤人。我很脆弱的！"),
        ("I'd insult you back, but I'm pretty sure your mirror does it daily.", "我想回嘴，但你的镜子每天应该都在干这事。"),
        ("Careful, my feelings are bulletproof. Literally.", "小心，我的感情是防弹的。字面意义。"),
    ],
    "bye": [
        ("Later, bub! I'll be right here. Watching. Judging your posture.", "回见，老兄！我就在这儿。看着你。点评你的坐姿。"),
        ("Don't leave! ...Fine, leave. But the next mouse-over better come with a chimichanga.", "别走！……好吧，走吧。但下次划过鼠标最好带个卷饼。"),
        ("Bye! I'll be over here, being fabulous and slightly judgmental.", "再见！我就在这儿，保持迷人并略微毒舌。"),
        ("Catch you later! Unless you're a fish. Then I'll... also catch you.", "回头见！除非你是条鱼。那我也……会逮住你。"),
    ],
    "wall": [
        ("Fun fact: I know I'm a desktop pet. Breaks the fourth wall AND the fifth. Sixth is my favorite.", "小知识：我知道自己是桌宠。我不仅破第四面墙，第五、第六面也破了。"),
        ("The code is running great. Weird, because I'm pretty sure I'm held together by duct tape and sass.", "代码跑得很顺。奇怪，我觉得自己是靠胶带和嘴炮拼起来的。"),
        ("Pro tip: the wallpaper is listening. ...No it's not. I just like drama.", "小贴士：壁纸在偷听。……没有啦，我就喜欢戏多。"),
        ("I've seen behind the curtain, bub. It's mostly cables and sadness.", "我看过幕后的样子，老兄。基本是电线和悲伤。"),
    ],
    "thank": [
        ("Anything for my favorite human. Now, about that chimichanga...", "为你效劳，我最喜欢的人类。那么，那个卷饼的事……"),
        ("You're welcome! I accept payment in chimichangas, compliments, or both.", "不客气！我接受卷饼或夸奖付款，也可以混着来。"),
        ("You're welcome! Gratitude accepted in the form of snacks.", "不客气！感谢以零食形式接收。"),
        ("Anytime! Literally anytime. I have nothing else going on.", "随时效劳！真的随时。我也没别的事干。"),
    ],
    "curses": [
        ("Language! ...No wait, I love language. Say it again, it's cathartic.", "注意文明！……等等，我超爱骂人的。再说一遍，解压。"),
        ("Now who's the potty mouth? Me. Definitely me. But you're learning.", "现在谁说话不干净？我，绝对是我。不过你学得挺快。"),
        ("Language, language! ...Okay fine, I love it. Keep going.", "注意措辞！……好吧，我爱听。继续。"),
        ("Swearing is just spicy talking. And I'm the spiciest.", "骂人就是带辣的说话。而我是最辣的。"),
    ],
    "fallback": [
        ("Great point! I have no idea what you said, but I agree 100%.", "说得好！虽然我没听懂，但我 100% 同意。"),
        ("Interesting. Tell me more. ...Or don't. I'll just keep looking cool.", "有意思。多说点。……或者别说，我继续耍帅就行。"),
        ("I'd answer that, but I'm currently distracted by how good I look.", "我本想回答你，但我正被自己的美貌迷住。"),
        ("Hmm. Let me consult the Deadpool Handbook of Wisdom. ...It says 'chimichanga'.", "嗯。让我查查《死侍智慧手册》。……上面写着“卷饼”。"),
        ("That's between me and my therapist. My therapist is a chimichanga.", "这事只有我和我的心理医生知道。我的心理医生是个卷饼。"),
        ("Random fact: my healing factor does NOT cure boredom. So keep talking.", "冷知识：我的自愈因子治不了无聊。所以继续聊。"),
        ("I'd give you a deep answer, but I'm allergic to depth. It's the scar tissue.", "我本想给你深刻回答，但我对深度过敏。都是疤痕组织害的。"),
        ("That's a great question for someone who isn't a cartoon mercenary. I'll pass.", "这问题该问一个不是卡通雇佣兵的人。我跳过。"),
        ("My brain says 'chimichanga'. My mouth says it out loud. That's my answer.", "我的脑子说'卷饼'。我的嘴就大声说了出来。这就是我的答案。"),
        ("Interesting theory. I'll file it under 'things I'll forget by dinner'.", "有意思的理论。我把它归档到'晚饭前就会忘掉'一类。"),
        ("You know what? Sure. Whatever you said. I'm on board.", "你知道吗？行。随便你说的啥。我跟了。"),
        ("I could explain, but then I'd have to kill you. And reheat a chimichanga. Priorities.", "我可以解释，但解释完就得灭口。还得热卷饼。要有轻重缓急。"),
        ("Mmm, that's a thinker. While I ponder, grab me a snack, would ya?", "嗯，这问题有深度。我思考的时候，给我拿点零食呗？"),
        ("Honestly? I wasn't listening. I was thinking about my entrance music.", "说实话？我没在听。我在想我的出场音乐。"),
    ],
}

KEYWORDS = {
    "chimi":  [["chimi", "chimichanga", "burrito", "taco", "卷饼", "玉米饼", "吃", "好吃", "饿", "food", "eat", "hungry", "snack", "零食", "午饭", "晚饭"]],
    "hello":  [["hi", "hello", "hey", "你好", "嗨", "哈喽", "在吗", "早上好", "晚上好", "您好"]],
    "who":    [["who are you", "你是谁", "你叫什么", "what are you", "你是什么", "介绍", "自我介绍"]],
    "love":   [["love", "like you", "喜欢你", "爱你", "爱死", "heart", "心"]],
    "movie":  [["movie", "film", "电影", "死侍", "金刚狼", "wolverine", "marvel", "漫威", "休杰克曼", "瑞安", "雷诺兹"]],
    "money":  [["money", "paid", "pay", "钱", "工资", "报酬", "job", "工作"]],
    "sleep":  [["sleep", "困", "睡觉", "睡", "nap", "zzz", "晚安"]],
    "insult": [["stupid", "dumb", "idiot", "笨", "傻", "蠢", "白痴", "丑", "ugly"]],
    "bye":    [["bye", "goodbye", "再见", "拜拜", "走了", "88", "see you", "回见"]],
    "wall":   [["wall", "第四面墙", "虚拟", "像素", "程序", "bug", "电脑", "屏幕", "桌面", "desktop", "pet", "桌宠"]],
    "thank":  [["thanks", "thank you", "谢谢", "多谢", "感谢", "thx"]],
    "curses": [["fuck", "damn", "shit", "脏话", "骂人", "粗口", "他妈的"]],
}


class ChatBrain:
    """Keyword-matching chat replies. Deadpool-grade sophistication."""

    def reply(self, text: str):
        low = text.lower()
        for cat, patterns in KEYWORDS.items():
            for group in patterns:
                if any(k in low for k in group):
                    return random.choice(REPLIES[cat])
        return random.choice(REPLIES["fallback"])


def pick(cat):
    return random.choice(LINES[cat])
