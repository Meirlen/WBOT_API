
IS_DEBUG_MODE =  False # for actions
TELEGRAM_IS_PROD = False 
TELEGRAM_IS_PROD = False 
TELEGRAM_IS_PROD = False 

ACTION_ENDPOINT = "http://localhost:5005" 

ADMIN_CHAT_ID = 2038418743 # the same 87471835157
ADMIN_CHAT_ID_2 = 5172316091 # the same 87711474766

# Telegram Settings
if TELEGRAM_IS_PROD:
    # Prod
    TELEGRAM_HTTP_ACCESS_TOKEN = '5350351478:AAGxTzWfuEBBmhKMxUin76kStfZSaE2Gny0'  # kkk09bot
    IS_DEBUG_MODE = False
else:    
    # # Debug
    TELEGRAM_HTTP_ACCESS_TOKEN = '5193584451:AAGth9M7cE5YteQW01Nb8h4ioGh-HT_9SjQ'  # MeirlenBot
    
ADMIN_HELP_FUNCTION = False

CONFIRM_YANDEX_BTN_TITLE = "🚕  Яндекс - 900 т"
CONFIRM_9_REGION_BTN_TITLE = "🚕  9 регион - 900 т"
CONFIRM_ALEM_BTN_TITLE = "🚕  Алем - 900 т"



CONFIRM_ORDER_BTN_TITLE = "🚕 Заказать"
ADD_ADDRESS_BTN_TITLE = "➕ Добавить адрес"
ADD_COMMENT_BTN_TITLE = "📝 Добавить комментарий"
CANCEL_BTN_TITLE = '⭕ Отмена'
CONFIRM_BTN_TITLE = '⚪ Завершить заказ'
CREATE_NEW_ORDER = 'Создать новый заказ'
CONFIRM_TEXT ="Хорошо"
ORDER_TAXI = '\U0001F695 Заказать такси'


TITLE_AFTER_CREATED_ORDER = '💁 <b>- Среднее время ожидания авто - 10 минут</b>'
DESC_AFTER_CREATED_ORDER = '_Чтобы заказать такси или добавить дополнительные опции нажмите на меню._'
TITLE_AFTER_CONFIRMED_ORDER = '💁 <b>- Заказ принят</b>'
DESC_AFTER_CONFIRMED_ORDER  = '_Идет поиск машины..._\n_Ожидайте сообщения с номером автомобиля_'
TITLE_MULTIPLE_ADDRESS_FOUND = 'Мы нашли несколько вариантов по вашему запросу.'
BOT_NO_COULD_NOT_CALC_COST_MESSAGE = '_____________'
BOT_CALC_COST_WARNING_MESSAGE = '\n\n_При формировании оплаты бот может ошибиться._'
BOT_ASK_TO_ADDRESS ='💁 <b>Куда едем?</b>\n\n'

# BODY_WHATSAPP_ASK_ADDRESS_FROM = '💁 *- Чтобы заказать такси напишите Откуда и Куда поедете?*\n\n Например: \n_«c 12 13 16 поедем на Восток 2»_\n_«с Алиханова 7 квартира 89 на цум»_\n\n'
BODY_WHATSAPP_ASK_ADDRESS_FROM = '💁 *- Откуда и Куда поедете?*'

TEMPLATE_START_TEXT = 'Поездка №'

# Zone names

M1 = 'майкудук нижний'
M2 = 'майкудук середина'
M2_1 = 'майкудук середина'
M2_2 = 'майкудук середина'
M3 = 'майкудук верхний'

M3_1 = 'майкудук верхний шахтерский поселок'

F = 'федоровка'    # P+' '+F: F+' '+S: F+' '+T:
F1 = 'федоровка 1'
F2 = 'федоровка 2'
F3 = 'федоровка 3'


C = "город"
U = "юг"

MI = 'михайловка' # used only on case MI+' '+T:
MI1 = 'михайловка 1'
MI2 = 'михайловка 2'
MI3 = 'михайловка 3'

S = 'сортировка'
R = 'рынок'
P = 'пришахтинск'
T = 'темиртау'

HMK = 'хмк'