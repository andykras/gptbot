import locale

current_locale = locale.getdefaultlocale()
lang = current_locale[0] or "en_US"

messages = {
    "en_US": {
        "bot": {
            "your_tutor": "Your Assistant: `{tutor}`",
            "not_allowed": "*NOT ALLOWED*, id=`{id}`",
            "welcome": "Hi, *{name}*!\n```{id}```",
            "new_chat": "`Context cleared`",
            "new_tutor": "Select new Assistant:\n{tutors}",
            "error_in_the_code": "`error 42`"
        },
        "gpt": {
            "instructions": "Please address the user as {name}. The user has a premium account."
        }
    },
    "ru_RU": {
        "bot": {
            "your_tutor": "Ваш Ассистент: `{tutor}`",
            "not_allowed": "*НЕТ ДОСТУПА*, id=`{id}`",
            "welcome": "Привет, *{name}*!\n```{id}```",
            "new_chat": "`История очищена`",
            "new_tutor": "Выберите нового Ассистента:\n{tutors}",
            "error_in_the_code": "`ошибка 42`"
        },
        "gpt": {
            "instructions": "Пожалуйста, обращайтесь к пользователю как {name}. У пользователя премиум-аккаунт."
        }
    }
}


def _t(path, **kwargs):
  keys = path.split('.')
  translation = messages[lang]
  for key in keys:
    translation = translation[key]

  return translation.format(**kwargs)
