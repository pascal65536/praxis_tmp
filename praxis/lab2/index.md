# Лабораторная работа 2. Обработка файлов и извлечение URL

**POV:** Файлы содержат ссылки на социальные сети и посты в социальных сетях. Пользователи предоставляли отчеты о своей работе и вместо того, чтобы собрать все свои ссылки, привести их к единому виду и расположить в удобном для обработки виде, отчитывались как угодно. В одной строке несколько ссылок, причем могут не использовать никаких разделителей. Среди ссылок на соцсети могут встретиться ссылки на сайты учереждений. Ссылки могут дублироваться, потому что отчет присылали несколько раз. Вместе со ссылками на три основные соцсети vk, ok, tg добавляют ссылки на чаты в других месенджерах и соцсетях. Ссылки могут набирать руками и допускать ошибки, нужно отследить, что вместо https набрали hhtp или httpc - такие ссылки нужно привести к правильному виду.

## Задание

На вход программе поступает строка, она может быть пустая, может содержать ссылку или несколько ссылок. Могут встретиться надписи на русском языке, до или после ссылки может быть комментарий. Ссылки могут быть объединены в строку через пробел, запятую или склеены без разделителей.

Ссылки могут быть некорректными, по возможности их нужно "починить".

Не стремитесь сделать "универсальный код", пусть он решает только поставленные задачи.

В некоторых тяжелых случаях ссылка может испортить другую ссылку, если пользователь вставил одну внутрь другой. Тогда медицина здесь бессильна. Также поступим, если пользователь назвал свой паблик ВКонтакте "https...."

### Требования к реализации

Вы должны написать функцию, на вход которой подается строка, на выходе — список ссылок.

### Варианты

Весь пул проверочных данных вы можете посмотреть в файле [check.json](check.json)

| № Теста | Входные данные | Выходные данные |
|---------|----------------|-----------------|
| 1 | `https://t.me/tvoe_vremya_krsk/3194` | `["https://t.me/tvoe_vremya_krsk/3194"]` |
| 2 | `https://vk.com/feed?section=search&q=%23%D0%B2%D1%8B%D0%B1%D0%B8%D1%80%D0%B0%D0%B5%D0%BC` | `["https://vk.ru/feed"]` |
| 3 | `https://vk.com/wall-15812938?w=wall-15812938_7378%2Fall` | `["https://vk.ru/wall-15812938"]` |
| 4 | `Заведующий` | `[]` |
| 5 | `https://sun9-40.userapi.com/impg/TyZ_F7qWsS9NEQ-dkPOK_AbJvWVC9CCGNOr2xQ/m3KyIU5kpVg.jpg?size=605x807&quality=95&sign=2365625c827eae5ffdb8863686612c10&c_uniq_tag=LXhG0WRGo6SrokqGVarWb4r1vrIkg6wqDYi_GfqZwes&type=album` | `["https://sun9-40.userapi.com/impg/TyZ_F7qWsS9NEQ-dkPOK_AbJvWVC9CCGNOr2xQ/m3KyIU5kpVg.jpg"]` |
| 6 | `https://vk.com/wall-217205976_454    https://vk.com/wall-217205976_455` | `["https://vk.ru/wall-217205976_454", "https://vk.ru/wall-217205976_455"]` |
| 7 | `https://vk.com/wall-207862709_690  https://vk.com/wall-207862709_691  https://vk.com/wall-207862709_692  https://vk.com/wall-207862709_693  https://vk.com/wall-207862709_694` | `["https://vk.ru/wall-207862709_690", "https://vk.ru/wall-207862709_691", "https://vk.ru/wall-207862709_692", "https://vk.ru/wall-207862709_693", "https://vk.ru/wall-207862709_694"]` |
| 8 | `https://vk.com/public203552167?z=photo-203552167_457239773%2Falbum-203552167_00%2Frev` | `["https://vk.ru/public203552167"]` |
| 9 | `https://vk.com/club145371898?w=wall-145371https://vk.com/club145371898?w=wall-145371898_4153 898_4154` | `["https://vk.ru/club145371898", "https://vk.ru/club145371898"]` |
| 10 | `https://vk. com/zgrcekit` | `["https://vk.ru/zgrcekit"]` |
| 11 | `https://telesco.pe/rusmikola/807, https://t.me/, https://vk.com/raspopin_n?w=wall2713687_1282rusmikola/808,` | `["https://telesco.pe/rusmikola/807", "https://t.me/", "https://vk.ru/raspopin_n"]` |
| 12 | `https://vk.com/public211959405?w=wall-211959405_870` | `["https://vk.ru/public211959405"]` |
| 13 | `https://vk.com/digitalkrsk24?w=wall-19280849, https://t.me/kras_digital/2583, 4_3929 , https://ok.ru/digitalkrsk24/topic/156430883080384` | `["https://vk.ru/digitalkrsk24", "https://t.me/kras_digital/2583", "https://ok.ru/digitalkrsk24/topic/156430883080384"]` |
| 14 | `httpsvk.comclub192877911#:~:text=%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%BE%D0%B5%20%D1%81%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D0%B5%202024,%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D0%BF%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%D0%B2%D1%88%D0%B8%D1%85%D1%81%D1%8F` | `[]` |
| 15 | `https://vk.com/httpsvk.comclub211825265?w=wall-211825265_781` | `["https://vk.ru/"]` |
| 16 | `http://vk.com/public217731299` | `["https://vk.ru/public217731299"]` |
| 17 | `httpc://vk.com/public217383223` | `["https://vk.ru/public217383223"]` |
| 18 | `Https://vk.com/club217442327` | `["https://vk.ru/club217442327"]` |
| 19 | `https//vk.com/public217115339` | `["https://vk.ru/public217115339"]` |
| 20 | `https//vk.com/public217115339` | `["https://vk.ru/public217115339"]` |
| 21 | `Ссылка на официальную страницу` | `[]` |
| 22 | `https://vk.com/aod ms24` | `["https://vk.ru/aod"]` |
| 23 | `17 марта - последний день для голосования. Избирательные участки работают с 8.00 - 20.00  Каждый проголосовавший может принять участие в Викторине. Викторина посвящена 90-летию образования Красноярского края и направлена на вовлечение жителей в изучение природы, истории и культуры родного региона. Ознакомиться с условиями участия и полным списком победителей в викторине можно на сайте викторина2024.рф. На все интересующие вопросы ответят по телефону единой горячей линии: 8-800-100-14-24  #выбираемПрезидента #Красноярскийкрай` | `[]` |
| 24 | `после опубликования поста активную ссылку на него нужно разместитьь в гугл форме здесь https://docs.google.com/spreadsheets/d/1uQ2VkJ-Rp-zCh6x6trafNRF1hD3Tnn-Nqd45m_Y11Jg/edit?usp=sharing` | `["https://docs.google.com/spreadsheets/d/1uQ2VkJ-Rp-zCh6x6trafNRF1hD3Tnn-Nqd45m_Y11Jg/edit"]` |
| 25 | `1.  https://vk.com/public212981532?w=wall-212981532_557` | `["https://vk.ru/public212981532"]` |
| 26 | `https://vk.com/public217385721?w=wall-217385721_469,https://vk.com/public217385721?w=wall-217385721_470, https://vk.com/public217385721?w=wall-217385721_473 , https://vk.com/public217385721?w=wall-217385721_467` | `["https://vk.ru/public217385721", "https://vk.ru/public217385721", "https://vk.ru/public217385721", "https://vk.ru/public217385721"]` |
| 27 | `https://vk.com/httpsvk.comclub211825265?w=wall-211825265_781` | `["https://vk.ru/"]` |
| 28 | `https://vk.com/wall-207148281_1145 ;  https://vk.com/wall-207148281_1147 ;   https://vk.com/wall-207148281_1151 ; https://vk.com/wall-207148281_1168 ; https://vk.com/wall-207148281_1169` | `["https://vk.ru/wall-207148281_1145", "https://vk.ru/wall-207148281_1147", "https://vk.ru/wall-207148281_1151", "https://vk.ru/wall-207148281_1168", "https://vk.ru/wall-207148281_1169"]` |
| 29 | `• https://vk.com/wall-217094378_304` | `["https://vk.ru/wall-217094378_304"]` |
| 30 | `t.me/nazarovoofficially /8259` | `["https://t.me/nazarovoofficially"]` |
| 31 | `https://vk/com/wall-67295671_1462` | `["https://vk.ru/wall-67295671_1462"]` |
| 32 | `https://m.vk.ru/wall-213816528_739` | `["https://vk.ru/wall-213816528_739"]` |
| 33 | `https://m.ok.ru/profile/587443413302/statuses/156830459574326` | `["https://ok.ru/profile/587443413302/statuses/156830459574326"]` |
| 34 | `https://m.ok.ru/dk?st.cmd=altGroupMediaThemeComments&st.groupId=61519743942742&st.themeId=157164019817814&st.rf=off&_prevCmd=altGroupMain&tkn=4751&_cl.id=1710567085802&_clickLog=%5B%7B%22target%22%3A%22text%22%7D%2C%7B%22target%22%3A%22content%22%7D%2C%7B%22topicId%22%3A%22157164019817814%22%2C%22groupId%22%3A%2261519743942742%22%2C%22target%22%3A%22topicCard%22%7D%2C%7B%22feedPage%22%3A%221%22%2C%22topicId%22%3A%22157164019817814%22%2C%22feedPosition%22%3A%222%22%2C%22feedFeatures%22%3A%220c01b400020202ffffff0000ffff00000000000000010100800000ffff07000201b401d0f7a4%22%2C%22feedId%22%3A%22feedId_0302000037f3ae7c00560000ad5a8a689756%22%2C%22groupId%22%3A%2261519743942742%22%7D%2C%7B%22feedLocation%22%3A%22group%22%2C%22feedFilterId%22%3A%22101%22%2C%22offerLocation%22%3A%22FEED%22%7D%5D&_cl.sID=altGroupMain` | `["https://ok.ru/dk"]` |
| 35 | `https:vk.com/wail-212962227_377` | `["https://vk.ru/wail-212962227_377"]` |
| 36 | `https://sh4-achinsk-r04.gosweb.gosuslugi.ru/roditelyam-i-uchenikam/novosti/novosti_1289.html` | `["https://sh4-achinsk-r04.gosweb.gosuslugi.ru/roditelyam-i-uchenikam/novosti/novosti_1289.html"]` |
| 37 | `https://fast.vk.com/public213485744` | `["https://vk.ru/public213485744"]` |
| 38 | `https://ds-olenenok-norilsk-r04.gosweb.gosuslugi.ru/nash-detskiy-sad/novosti-i-sobytiya/golosuem-vsey-semey.html` | `["https://ds-olenenok-norilsk-r04.gosweb.gosuslugi.ru/nash-detskiy-sad/novosti-i-sobytiya/golosuem-vsey-semey.html"]` |
| 39 | `https://vk.com/wall-212762540_1155` | `["https://vk.ru/wall-212762540_1155"]` |
| 40 | `https://vk.com/public217438341?w=wall-217438341_203` | `["https://vk.ru/public217438341"]` |
| 41 | `https://vk.com/wall-217644230_33` | `["https://vk.ru/wall-217644230_33"]` |
| 42 | `https://vk.com/public172596821?w=wall-172596821_5701` | `["https://vk.ru/public172596821"]` |

### Проверяющая система

Проверяющая система работает с JSON-файлом. Код будет дан. Дополнительно ваш код будет проверен на больших файлах.

### PS

Предложите способ как в дальнейшем избежать получения подобных ссылок

[Скачать стенд для этой работы](https://github.com/pascal65536/praxis_tmp/tree/main/praxis/lab2)