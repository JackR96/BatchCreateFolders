import os
import re

# 将您提供的目录结构文本粘贴到这里
# 使用三引号可以方便地处理多行字符串
DIRECTORY_STRUCTURE_TEXT = """
世界国家目录/
├── 亚洲/
│   ├── 东亚/
│   │   ├── jp 81 日本 Japan
│   │   ├── kr 82 韩国 South Korea
│   │   ├── cn 86 中国 China
│   │   ├── kp 850 朝鲜 North Korea
│   │   ├── hk 852 香港 Hong Kong
│   │   ├── mo 853 澳门 Macau
│   │   ├── tw 886 台湾 Taiwan
│   │   └── mn 976 蒙古 Mongolia
│   ├── 东南亚/
│   │   ├── my 60 马来西亚 Malaysia
│   │   ├── id 62 印度尼西亚 Indonesia
│   │   ├── ph 63 菲律宾 Philippines
│   │   ├── sg 65 新加坡 Singapore
│   │   ├── th 66 泰国 Thailand
│   │   ├── vn 84 越南 Vietnam
│   │   ├── kh 855 柬埔寨 Cambodia
│   │   ├── la 856 老挝 Laos
│   │   ├── mm 95 缅甸 Myanmar
│   │   ├── bn 673 文莱 Brunei
│   │   └── tl 670 东帝汶 Timor-Leste
│   ├── 南亚/
│   │   ├── bd 880 孟加拉国 Bangladesh
│   │   ├── in 91 印度 India
│   │   ├── pk 92 巴基斯坦 Pakistan
│   │   ├── af 93 阿富汗 Afghanistan
│   │   ├── lk 94 斯里兰卡 Sri Lanka
│   │   ├── ir 98 伊朗 Iran
│   │   ├── mv 960 马尔代夫 Maldives
│   │   ├── bt 975 不丹 Bhutan
│   │   └── np 977 尼泊尔 Nepal
│   ├── 中亚/
│   │   ├── kz 7 哈萨克斯坦 Kazakhstan
│   │   ├── tj 992 塔吉克斯坦 Tajikistan
│   │   ├── tm 993 土库曼斯坦 Turkmenistan
│   │   ├── kg 996 吉尔吉斯斯坦 Kyrgyzstan
│   │   └── uz 998 乌兹别克斯坦 Uzbekistan
│   └── 中东 (西亚)/
│       ├── kw 965 科威特 Kuwait
│       ├── sa 966 沙特阿拉伯 Saudi Arabia
│       ├── ye 967 也门 Yemen
│       ├── om 968 阿曼 Oman
│       ├── ps 970 巴勒斯坦 Palestine
│       ├── ae 971 阿拉伯联合酋长国 United Arab Emirates
│       ├── il 972 以色列 Israel
│       ├── bh 973 巴林 Bahrain
│       ├── qa 974 卡塔尔 Qatar
│       ├── lb 961 黎巴嫩 Lebanon
│       ├── jo 962 约旦 Jordan
│       ├── sy 963 叙利亚 Syria
│       └── iq 964 伊拉克 Iraq
├── 欧洲/
│   ├── 西欧/
│   │   ├── nl 31 荷兰 Netherlands
│   │   ├── be 32 比利时 Belgium
│   │   ├── fr 33 法国 France
│   │   ├── uk 44 英国 United Kingdom
│   │   ├── de 49 德国 Germany
│   │   ├── ch 41 瑞士 Switzerland
│   │   ├── at 43 奥地利 Austria
│   │   ├── lu 352 卢森堡 Luxembourg
│   │   ├── ie 353 爱尔兰 Ireland
│   │   ├── li 423 列支敦士登 Liechtenstein
│   │   └── mc 377 摩纳哥 Monaco
│   ├── 北欧/
│   │   ├── dk 45 丹麦 Denmark
│   │   ├── se 46 瑞典 Sweden
│   │   ├── no 47 挪威 Norway
│   │   ├── is 354 冰岛 Iceland
│   │   └── fi 358 芬兰 Finland
│   ├── 东欧/
│   │   ├── ru 7 俄罗斯 Russia
│   │   ├── cz 420 捷克共和国 Czech Republic
│   │   ├── sk 421 斯洛伐克 Slovakia
│   │   ├── hu 36 匈牙利 Hungary
│   │   ├── ro 40 罗马尼亚 Romania
│   │   ├── pl 48 波兰 Poland
│   │   ├── bg 359 保加利亚 Bulgaria
│   │   ├── ua 380 乌克兰 Ukraine
│   │   ├── by 375 白俄罗斯 Belarus
│   │   ├── md 373 摩尔多瓦 Moldova
│   │   ├── lt 370 立陶宛 Lithuania
│   │   ├── lv 371 拉脱维亚 Latvia
│   │   └── ee 372 爱沙尼亚 Estonia
│   └── 南欧/
│       ├── gr 30 希腊 Greece
│       ├── it 39 意大利 Italy
│       ├── pt 351 葡萄牙 Portugal
│       ├── es 34 西班牙 Spain
│       ├── tr 90 土耳其 Turkey
│       ├── al 355 阿尔бания Albania
│       ├── mt 356 马耳他 Malta
│       ├── cy 357 塞浦路斯 Cyprus
│       ├── sm 378 圣马力诺 San Marino
│       ├── va 379 梵蒂冈城 Vatican City
│       ├── rs 381 塞尔维亚 Serbia
│       ├── me 382 黑山 Montenegro
│       ├── hr 385 克罗地亚 Croatia
│       ├── si 386 斯洛文尼亚 Slovenia
│       ├── ba 387 波斯尼亚和黑塞哥维那 Bosnia and Herzegovina
│       ├── mk 389 北马其顿 North Macedonia
│       └── ad 376 安道尔 Andorra
├── 北美洲/
│   ├── us 1 美国 United States
│   ├── ca 1 加拿大 Canada
│   ├── gl 299 格陵兰 Greenland
│   └── pm 508 圣皮埃尔和密克隆 Saint Pierre and Miquelon
├── 拉美/
│   ├── 中美洲/
│   │   ├── bz 501 伯利兹 Belize
│   │   ├── gt 502 危地马拉 Guatemala
│   │   ├── sv 503 萨尔瓦多 El Salvador
│   │   ├── hn 504 洪都拉斯 Honduras
│   │   ├── ni 505 尼加拉瓜 Nicaragua
│   │   ├── cr 506 哥斯达黎加 Costa Rica
│   │   ├── pa 507 巴拿马 Panama
│   │   └── mx 52 墨西哥 Mexico
│   ├── 加勒比地区/
│   │   ├── ht 509 海地 Haiti
│   │   ├── cu 53 古巴 Cuba
│   │   ├── bs 1-242 巴哈马 Bahamas
│   │   ├── bb 1-246 巴巴多斯 Barbados
│   │   ├── ag 1-268 安提瓜和巴布达 Antigua and Barbuda
│   │   ├── gd 1-473 格林纳达 Grenada
│   │   ├── lc 1-758 圣卢西亚 Saint Lucia
│   │   ├── dm 1-767 多米尼克 Dominica
│   │   ├── vc 1-784 圣文森特和格林纳丁斯 Saint Vincent and the Grenadines
│   │   ├── do 1-809 多米尼加共和国 Dominican Republic
│   │   ├── tt 1-868 特立尼达和多巴哥 Trinidad and Tobago
│   │   ├── kn 1-869 圣基茨和尼维斯 Saint Kitts and Nevis
│   │   └── jm 1-876 牙买加 Jamaica
│   └── 南美洲/
│       ├── pe 51 秘鲁 Peru
│       ├── ar 54 阿根廷 Argentina
│       ├── br 55 巴西 Brazil
│       ├── cl 56 智利 Chile
│       ├── co 57 哥伦比亚 Colombia
│       ├── ve 58 委内瑞拉 Venezuela
│       ├── bo 591 玻利维亚 Bolivia
│       ├── gy 592 圭亚那 Guyana
│       ├── ec 593 厄瓜多尔 Ecuador
│       ├── py 595 巴拉圭 Paraguay
│       ├── sr 597 苏里南 Suriname
│       └── uy 598 乌拉圭 Uruguay
├── 大洋洲/
│   ├── au 61 澳大利亚 Australia
│   ├── nz 64 新西兰 New Zealand
│   ├── nr 674 瑙鲁 Nauru
│   ├── pg 675 巴布亚新几内亚 Papua new Guinea
│   ├── to 676 汤加 Tonga
│   ├── sb 677 所罗门群岛 Solomon Islands
│   ├── vu 678 瓦努阿图 Vanuatu
│   ├── fj 679 斐济 Fiji
│   ├── pw 680 帕劳 Palau
│   ├── ws 685 萨摩亚 Samoa
│   ├── ki 686 基里巴斯 Kiribati
│   ├── tv 688 图瓦卢 Tuvalu
│   ├── fm 691 密克罗尼西亚 Micronesia
│   └── mh 692 马绍尔群岛 Marshall Islands
└── 非洲/
    ├── 北非/
    │   ├── eg 20 埃及 Egypt
    │   ├── ma 212 摩洛哥 Morocco
    │   ├── dz 213 阿尔及利亚 Algeria
    │   ├── tn 216 突尼斯 Tunisia
    │   ├── ly 218 利比亚 Libya
    │   └── sd 249 苏丹 Sudan
    ├── 东非/
    │   ├── mu 230 毛里求斯 Mauritius
    │   ├── ss 211 南苏丹 South Sudan
    │   ├── tz 251 坦桑尼亚 Tanzania
    │   ├── rw 250 卢旺达 Rwanda
    │   ├── so 252 索马里 Somalia
    │   ├── dj 253 吉布提 Djibouti
    │   ├── ke 254 肯尼亚 Kenya
    │   ├── ug 256 乌干达 Uganda
    │   ├── bi 257 布隆迪 Burundi
    │   ├── mz 258 莫桑比克 Mozambique
    │   ├── zm 260 赞比亚 Zambia
    │   ├── mg 261 马达加斯加 Madagascar
    │   ├── zw 263 津巴布韦 Zimbabwe
    │   ├── mw 265 马拉维 Malawi
    │   ├── km 269 科摩罗 Comoros
    │   ├── er 291 厄立特里亚 Eritrea
    │   ├── sc 248 塞舌尔 Seychelles
    │   └── et 251 埃塞俄比亚 Ethiopia
    ├── 中非/
    │   ├── td 235 乍得 Chad
    │   ├── cf 236 中非共和国 Central African Republic
    │   ├── cm 237 喀麦隆 Cameroon
    │   ├── st 239 圣多美和普林西比 Sao Tome and Principe
    │   ├── gq 240 赤道几内亚 Equatorial Guinea
    │   ├── ga 241 加蓬 Gabon
    │   ├── cg 242 刚果（布） Congo, Republic of the
    │   ├── cd 243 刚果（金） Congo, Democratic Republic of the
    │   └── ao 244 安哥拉 Angola
    ├── 西非/
    │   ├── gm 220 冈比亚 Gambia
    │   ├── sn 221 塞内加尔 Senegal
    │   ├── mr 222 毛里塔尼亚 Mauritania
    │   ├── ml 223 马里 Mali
    │   ├── gn 224 几内亚 Guinea
    │   ├── ci 225 科特迪瓦 Côte d'Ivoire
    │   ├── bf 226 布基纳法索 Burkina Faso
    │   ├── ne 227 尼日尔 Niger
    │   ├── tg 228 多哥 Togo
    │   ├── bj 229 贝宁 Benin
    │   ├── lr 231 利比里亚 Liberia
    │   ├── sl 232 塞拉利昂 Sierra Leone
    │   ├── gh 233 加纳 Ghana
    │   ├── ng 234 尼日利亚 Nigeria
    │   ├── cv 238 佛得角 Cabo Verde
    │   └── gw 245 几内亚比绍 Guinea-Bissau
    └── 南非/
        ├── za 27 南非 South Africa
        ├── na 264 纳米比亚 Namibia
        ├── ls 266 莱索托 Lesotho
        ├── bw 267 博茨瓦纳 Botswana
        └── sz 268 斯威士兰 Eswatini
"""

def create_directories_from_text(structure_text):
    """
    解析文本格式的目录树并创建实际的文件夹。
    """
    lines = structure_text.strip().split('\n')
    
    # 获取并创建根目录
    root_dir = lines[0].strip().strip('/')
    if not root_dir:
        print("错误：无法确定根目录。")
        return
        
    print(f"创建根目录: {root_dir}")
    os.makedirs(root_dir, exist_ok=True)
    
    # 使用一个栈来追踪当前的路径
    # 栈中每个元素代表一层目录名
    path_stack = [root_dir]

    for line in lines[1:]:
        # 使用正则表达式匹配前缀（包含所有空格和特殊字符）
        match = re.match(r'([│├└\s─]*)', line)
        prefix_len = len(match.group(1)) if match else 0
        
        # 目录层级深度由前缀长度决定，每4个字符为一级
        depth = prefix_len // 4
        
        # 提取目录名
        # 去掉前缀，并去除首尾的空格和可能存在的'/'
        dir_name = line[prefix_len:].strip().strip('/')
        
        # 根据当前深度调整路径栈，确保父目录正确
        # 深度为1时，栈应只包含根目录（长度为1）
        # 深度为2时，栈应包含根目录和1级目录（长度为2）
        while len(path_stack) > depth:
            path_stack.pop()
            
        # 构建当前要创建的完整路径
        current_path = os.path.join(*path_stack, dir_name)
        
        # 创建目录
        try:
            os.makedirs(current_path, exist_ok=True)
            print(f"已创建: {current_path}")
        except OSError as e:
            print(f"创建失败: {current_path}\n错误: {e}")
            # 如果创建失败，可能包含非法字符，跳过此行
            continue

        # 将当前目录名压入栈中，作为后续子目录的父路径
        path_stack.append(dir_name)

    print("\n所有目录创建完成！")

if __name__ == "__main__":
    create_directories_from_text(DIRECTORY_STRUCTURE_TEXT)
