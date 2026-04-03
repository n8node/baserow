"""
Seed migration: replace placeholder landing blocks with a full baserow.io-style
landing page (both Russian and English locales).
"""

import json

from django.db import migrations


def _items(obj):
    """Return a JSON-serialisable dict (extra_data field)."""
    return obj


def seed(apps, schema_editor):
    LandingBlock = apps.get_model("core", "LandingBlock")
    LandingBlock.objects.all().delete()

    RU = "ru"
    EN = "en"

    # ── Russian blocks ───────────────────────────────────────────────────

    ru_blocks = [
        # 0 ─ Hero
        dict(
            order=0,
            locale=RU,
            enabled=True,
            block_type="hero",
            title="Платформа для совместной работы с данными",
            subtitle="Организуйте данные, создавайте приложения и автоматизируйте бизнес-процессы — без ущерба контролю, безопасности и приватности.",
            body="",
            image_url="",
            primary_cta_label="Начать бесплатно",
            primary_cta_url="/signup",
            secondary_cta_label="Связаться с нами",
            secondary_cta_url="/login",
            extra_data=_items(
                {
                    "badge": "Мы гордимся европейскими корнями",
                    "self_host_text": "Хотите развернуть у себя?",
                    "self_host_links": [
                        {"label": "Docker", "url": "https://baserow.io/docs/installation/install-with-docker"},
                        {"label": "Helm", "url": "https://baserow.io/docs/installation/install-with-helm"},
                    ],
                }
            ),
        ),
        # 1 ─ Product tabs
        dict(
            order=1,
            locale=RU,
            enabled=True,
            block_type="product_tabs",
            title="",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "tabs": [
                        {
                            "label": "Базы данных",
                            "icon": "📊",
                            "image": "",
                            "sidebar": [
                                {"icon": "📋", "label": "Управление рисками"},
                                {"icon": "✅", "label": "Управление задачами"},
                                {"icon": "📈", "label": "ESG"},
                                {"icon": "📣", "label": "Маркетинг"},
                                {"icon": "👥", "label": "CRM"},
                                {"icon": "🛒", "label": "Закупки"},
                                {"icon": "🏭", "label": "Производство"},
                            ],
                        },
                        {
                            "label": "Приложения",
                            "icon": "📱",
                            "image": "",
                            "sidebar": [],
                        },
                        {
                            "label": "Дашборды",
                            "icon": "📊",
                            "image": "",
                            "sidebar": [],
                        },
                        {
                            "label": "Автоматизации",
                            "icon": "⚡",
                            "badge": "Новое",
                            "image": "",
                            "sidebar": [],
                        },
                    ]
                }
            ),
        ),
        # 2 ─ Logos
        dict(
            order=2,
            locale=RU,
            enabled=True,
            block_type="logos",
            title="Выбор организаций, ценящих приватность, контроль и безопасность",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"src": "https://baserow.io/assets/images/logos/rbc.svg", "alt": "RBC"},
                        {"src": "https://baserow.io/assets/images/logos/capgemini.svg", "alt": "Capgemini"},
                        {"src": "https://baserow.io/assets/images/logos/charite.svg", "alt": "Charité"},
                        {"src": "https://baserow.io/assets/images/logos/and-e.svg", "alt": "AND-E"},
                        {"src": "https://baserow.io/assets/images/logos/believe.svg", "alt": "Believe"},
                    ]
                }
            ),
        ),
        # 3 ─ Badges
        dict(
            order=3,
            locale=RU,
            enabled=True,
            block_type="badges",
            title="",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "ratings_title": "Высший рейтинг от пользователей",
                    "ratings": [
                        {"src": "https://baserow.io/assets/images/badges/capterra-4-7.svg", "alt": "Capterra 4.7"},
                        {"src": "https://baserow.io/assets/images/badges/software-advice-4-8.svg", "alt": "Software Advice 4.8"},
                        {"src": "https://baserow.io/assets/images/badges/getapp-user-reviews.svg", "alt": "GetApp"},
                    ],
                    "certifications_title": "Сертификация защиты данных",
                    "certifications": [
                        {"src": "https://baserow.io/assets/images/badges/gdpr.svg", "label": "GDPR", "alt": "GDPR"},
                        {"src": "https://baserow.io/assets/images/badges/hipaa.svg", "label": "HIPAA", "alt": "HIPAA"},
                        {"src": "https://baserow.io/assets/images/badges/soc2.svg", "label": "SOC 2 Type II", "alt": "SOC 2"},
                    ],
                }
            ),
        ),
        # 4 ─ Deployment
        dict(
            order=4,
            locale=RU,
            enabled=True,
            block_type="deployment",
            title="Варианты развёртывания",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "options": [
                        {"icon": "☁️", "title": "Облако Baserow", "description": ""},
                        {"icon": "🖥️", "title": "Self-hosted (on-premise)", "description": "Полный контроль над инфраструктурой"},
                        {"icon": "🔒", "title": "Управляемый инстанс", "description": "По запросу"},
                    ]
                }
            ),
        ),
        # 5 ─ AI Assistant
        dict(
            order=5,
            locale=RU,
            enabled=True,
            block_type="section_image",
            title="Скажите Baserow что вам нужно — он построит это за вас",
            subtitle="Познакомьтесь с Kuma — вашим AI-ассистентом. Опишите данные, которыми хотите управлять, и Kuma построит всё сам.",
            body="",
            image_url="",
            primary_cta_label="Узнать о Kuma",
            primary_cta_url="#",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items({}),
        ),
        # 6 ─ How It Works
        dict(
            order=6,
            locale=RU,
            enabled=True,
            block_type="how_it_works",
            title="Как это работает",
            subtitle="Импортируйте данные из таблиц и инструментов, управляйте ими в одном месте. Автоматизируйте процессы, подключайте интеграции и создавайте приложения без кода.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "columns": [
                        {
                            "title": "Источники данных",
                            "items": [
                                {"icon": "🔧", "title": "Ваши инструменты", "description": "", "tags": []},
                                {"icon": "🌐", "title": "Внешние источники", "description": "", "tags": ["CSV", "XML", "JSON"]},
                            ],
                        },
                        {
                            "title": "Рабочие процессы",
                            "items": [
                                {"icon": "⚡", "title": "Нативные автоматизации", "description": "Конструктор автоматизаций", "tags": ["HTTP", "Email", "Webhooks"]},
                                {"icon": "🔗", "title": "Сторонние", "description": "", "tags": []},
                            ],
                        },
                        {
                            "title": "Интуитивные интерфейсы",
                            "items": [
                                {"icon": "📊", "title": "Базы данных", "description": "Визуализация и совместная работа", "tags": ["Таблица", "Канбан", "Календарь", "Форма"]},
                                {"icon": "📱", "title": "Приложения", "description": "Создавайте без кода", "tags": []},
                                {"icon": "🤖", "title": "AI + агенты", "description": "Добавьте AI в процессы", "tags": ["AI Field", "MCP Server"]},
                            ],
                        },
                    ]
                }
            ),
        ),
        # 7 ─ Build custom apps
        dict(
            order=7,
            locale=RU,
            enabled=True,
            block_type="section_image",
            title="Создавайте приложения под свои задачи",
            subtitle="Составляйте страницы, дашборды и рабочие процессы поверх данных — без написания кода.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "sidebar": [
                        {"icon": "📋", "label": "Управление рисками"},
                        {"icon": "✅", "label": "Управление задачами"},
                        {"icon": "📈", "label": "ESG"},
                        {"icon": "📣", "label": "Маркетинг"},
                        {"icon": "👥", "label": "CRM"},
                        {"icon": "🛒", "label": "Закупки"},
                        {"icon": "🏭", "label": "Производство"},
                    ]
                }
            ),
        ),
        # 8 ─ Automations
        dict(
            order=8,
            locale=RU,
            enabled=True,
            block_type="automations",
            title="Автоматизируйте рабочие процессы, чтобы исключить ручной труд и ошибки",
            subtitle="Упрощайте задачи с помощью no-code воркфлоу, настраиваемых под ваши потребности.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"icon": "🔀", "title": "Визуальная логика", "description": "С триггерами, ветвлениями, условиями и циклами"},
                        {"icon": "🔌", "title": "Бесшовные интеграции", "description": "HTTP, email, webhooks и сторонние коннекторы"},
                        {"icon": "📝", "title": "Логи для аудита", "description": "Соответствие требованиям комплаенса"},
                    ]
                }
            ),
        ),
        # 9 ─ Dashboards
        dict(
            order=9,
            locale=RU,
            enabled=True,
            block_type="section_image",
            title="Визуализируйте данные с помощью дашбордов",
            subtitle="Создавайте графики для отслеживания прогресса и коммуникации с руководством.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items({}),
        ),
        # 10 ─ Templates
        dict(
            order=10,
            locale=RU,
            enabled=True,
            block_type="templates_grid",
            title="Готовые шаблоны решений",
            subtitle="Превращайте таблицы в кастомные инструменты.",
            body="",
            image_url="",
            primary_cta_label="Смотреть все решения",
            primary_cta_url="#",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"title": "Управление задачами", "icon": "✅", "image": "", "url": "#"},
                        {"title": "Управление проектами", "icon": "📊", "image": "", "url": "#"},
                        {"title": "Оценка и управление рисками", "icon": "⚠️", "image": "", "url": "#"},
                        {"title": "Рекламные кампании", "icon": "📣", "image": "", "url": "#"},
                        {"title": "ESG Management", "icon": "🌱", "image": "", "url": "#"},
                        {"title": "GEMBA Walks", "icon": "🏭", "image": "", "url": "#"},
                    ]
                }
            ),
        ),
        # 11 ─ Why Baserow
        dict(
            order=11,
            locale=RU,
            enabled=True,
            block_type="features_grid",
            title="Почему Baserow?",
            subtitle="Открытая платформа с гибкостью, простотой использования, безопасностью и лучшим соотношением цена/качество.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"icon_emoji": "📊", "title": "Замена электронных таблиц", "description": "Управляйте данными между командами в реальном времени"},
                        {"icon_emoji": "💻", "title": "Кастомные решения", "description": "Создавайте бизнес-приложения быстрее и дешевле"},
                        {"icon_emoji": "🔒", "title": "Управление и соответствие", "description": "Управление данными и безопасность"},
                        {"icon_emoji": "☁️", "title": "Облако или self-hosted", "description": "Безопасность и масштабируемость"},
                        {"icon_emoji": "📖", "title": "Открытый исходный код", "description": "Без привязки к вендору"},
                        {"icon_emoji": "💰", "title": "Лучшая цена", "description": "Управляйте затратами на любом масштабе"},
                    ]
                }
            ),
        ),
        # 12 ─ Comparison
        dict(
            order=12,
            locale=RU,
            enabled=True,
            block_type="comparison",
            title="Открытая альтернатива Airtable",
            subtitle="Получите всё лучшее от Airtable — без недостатков.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "our_name": "Baserow",
                    "competitor": "Airtable",
                    "items": [
                        {"feature": "Открытый исходный код", "us": True, "us_text": "Открытый исходный код", "them": False, "them_text": "Закрытый исходный код"},
                        {"feature": "Облако + self-hosted", "us": True, "us_text": "Облако + self-hosted", "them": False, "them_text": "Без self-hosted"},
                        {"feature": "Конкурентные цены", "us": True, "us_text": "Конкурентные цены", "them": False, "them_text": "Дороже"},
                        {"feature": "Безлимитная масштабируемость", "us": True, "us_text": "Безлимитная масштабируемость (self-hosted)", "them": False, "them_text": "Низкие лимиты строк даже в enterprise"},
                        {"feature": "API-first", "us": True, "us_text": "API-first: каждая функция = endpoint", "them": False, "them_text": "Ограниченный API"},
                        {"feature": "Кастомизация плагинами", "us": True, "us_text": "Кастомизация фронтенд и бэкенд плагинами", "them": False, "them_text": "Только фронтенд расширения"},
                        {"feature": "Стабильность на масштабе", "us": True, "us_text": "Быстрый и стабильный даже на масштабе", "them": False, "them_text": ""},
                        {"feature": "GDPR, HIPAA, SOC 2", "us": True, "us_text": "GDPR, HIPAA и SOC 2 compliant", "them": False, "them_text": ""},
                        {"feature": "Конструктор приложений", "us": True, "us_text": "Мощный конструктор приложений", "them": False, "them_text": ""},
                    ],
                }
            ),
        ),
        # 13 ─ Testimonials
        dict(
            order=13,
            locale=RU,
            enabled=True,
            block_type="testimonials",
            title="Готов для enterprise — для всех команд и отраслей",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {
                            "quote": "Нам нравится скорость развёртывания и простота платформы.",
                            "name": "Cathy Tondu",
                            "role": "Digital Product Manager",
                            "logo": "",
                            "avatar": "",
                        },
                        {
                            "quote": "Мы используем Baserow как единственный источник истины для политик и инцидентов. Нам нравится простота, гибкость и безопасность.",
                            "name": "David Porter",
                            "role": "Vice President, Group Risk Management",
                            "logo": "",
                            "avatar": "",
                        },
                        {
                            "quote": "Baserow — ключевой технологический партнёр для all-in-one платформы наших агентов по недвижимости.",
                            "name": "Bryn Humble",
                            "role": "Chief Product Officer",
                            "logo": "",
                            "avatar": "",
                        },
                    ]
                }
            ),
        ),
        # 14 ─ CTA
        dict(
            order=14,
            locale=RU,
            enabled=True,
            block_type="cta",
            title="Готовы взять данные под контроль?",
            subtitle="Начните своё путешествие с Baserow сегодня.",
            body="",
            image_url="",
            primary_cta_label="Зарегистрироваться бесплатно",
            primary_cta_url="/signup",
            secondary_cta_label="Связаться с нами",
            secondary_cta_url="/login",
            extra_data=_items({"dark": True}),
        ),
        # 15 ─ Footer
        dict(
            order=15,
            locale=RU,
            enabled=True,
            block_type="footer",
            title="",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "columns": [
                        {
                            "title": "Компания",
                            "links": [
                                {"label": "Вакансии", "url": "#"},
                                {"label": "FAQ", "url": "#"},
                                {"label": "Партнёры", "url": "#"},
                                {"label": "Контакты", "url": "#"},
                                {"label": "Статус", "url": "#"},
                            ],
                        },
                        {
                            "title": "Платформа",
                            "links": [
                                {"label": "Шаблоны", "url": "#"},
                                {"label": "Цены", "url": "#"},
                                {"label": "Сообщество", "url": "#"},
                                {"label": "База знаний", "url": "#"},
                                {"label": "Интеграции", "url": "#"},
                            ],
                        },
                        {
                            "title": "Блог",
                            "links": [
                                {"label": "Релизы Baserow", "url": "#"},
                                {"label": "Airtable vs. Baserow", "url": "#"},
                                {"label": "Open-source альтернативы", "url": "#"},
                            ],
                        },
                        {
                            "title": "Для разработчиков",
                            "links": [
                                {"label": "Документация", "url": "#"},
                                {"label": "API", "url": "#"},
                                {"label": "OpenAPI", "url": "#"},
                            ],
                        },
                    ],
                    "newsletter": {
                        "title": "Подпишитесь на рассылку",
                        "description": "Будьте в курсе последних новостей и релизов.",
                        "placeholder": "Ваш email",
                        "button": "Подписаться",
                    },
                    "copyright": "© 2026 Baserow. Все права защищены.",
                    "legal_links": [
                        {"label": "Условия использования", "url": "#"},
                        {"label": "Политика конфиденциальности", "url": "#"},
                    ],
                    "social_links": [],
                }
            ),
        ),
    ]

    # ── English blocks ───────────────────────────────────────────────────

    en_blocks = [
        # 0 ─ Hero
        dict(
            order=0,
            locale=EN,
            enabled=True,
            block_type="hero",
            title="The data collaboration platform for teams",
            subtitle="Organize your data, build powerful applications and automate business processes — without ever sacrificing control, compliance, privacy and security.",
            body="",
            image_url="",
            primary_cta_label="Get started. It's free!",
            primary_cta_url="/signup",
            secondary_cta_label="Contact sales",
            secondary_cta_url="/login",
            extra_data=_items(
                {
                    "badge": "We're proudly European",
                    "self_host_text": "Prefer to self host?",
                    "self_host_links": [
                        {"label": "Docker", "url": "https://baserow.io/docs/installation/install-with-docker"},
                        {"label": "AWS", "url": "#"},
                        {"label": "Helm", "url": "https://baserow.io/docs/installation/install-with-helm"},
                    ],
                }
            ),
        ),
        # 1 ─ Product tabs
        dict(
            order=1,
            locale=EN,
            enabled=True,
            block_type="product_tabs",
            title="",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "tabs": [
                        {
                            "label": "Databases",
                            "icon": "📊",
                            "image": "",
                            "sidebar": [
                                {"icon": "📋", "label": "Risk Management"},
                                {"icon": "✅", "label": "Task Management"},
                                {"icon": "📈", "label": "ESG"},
                                {"icon": "📣", "label": "Marketing"},
                                {"icon": "👥", "label": "CRM"},
                                {"icon": "🛒", "label": "Purchasing"},
                                {"icon": "🏭", "label": "Manufacturing"},
                            ],
                        },
                        {"label": "Applications", "icon": "📱", "image": "", "sidebar": []},
                        {"label": "Dashboards", "icon": "📊", "image": "", "sidebar": []},
                        {"label": "Automations", "icon": "⚡", "badge": "New", "image": "", "sidebar": []},
                    ]
                }
            ),
        ),
        # 2 ─ Logos
        dict(
            order=2,
            locale=EN,
            enabled=True,
            block_type="logos",
            title="Chosen by organizations that value privacy, control, and compliance",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"src": "https://baserow.io/assets/images/logos/rbc.svg", "alt": "RBC"},
                        {"src": "https://baserow.io/assets/images/logos/capgemini.svg", "alt": "Capgemini"},
                        {"src": "https://baserow.io/assets/images/logos/charite.svg", "alt": "Charité"},
                        {"src": "https://baserow.io/assets/images/logos/and-e.svg", "alt": "AND-E"},
                        {"src": "https://baserow.io/assets/images/logos/believe.svg", "alt": "Believe"},
                    ]
                }
            ),
        ),
        # 3 ─ Badges
        dict(
            order=3,
            locale=EN,
            enabled=True,
            block_type="badges",
            title="",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "ratings_title": "Top-rated by users",
                    "ratings": [
                        {"src": "https://baserow.io/assets/images/badges/capterra-4-7.svg", "alt": "Capterra 4.7"},
                        {"src": "https://baserow.io/assets/images/badges/software-advice-4-8.svg", "alt": "Software Advice 4.8"},
                        {"src": "https://baserow.io/assets/images/badges/getapp-user-reviews.svg", "alt": "GetApp"},
                    ],
                    "certifications_title": "Certified for data protection",
                    "certifications": [
                        {"src": "https://baserow.io/assets/images/badges/gdpr.svg", "label": "GDPR", "alt": "GDPR"},
                        {"src": "https://baserow.io/assets/images/badges/hipaa.svg", "label": "HIPAA", "alt": "HIPAA"},
                        {"src": "https://baserow.io/assets/images/badges/soc2.svg", "label": "SOC 2 Type II", "alt": "SOC 2"},
                    ],
                }
            ),
        ),
        # 4 ─ Deployment
        dict(
            order=4,
            locale=EN,
            enabled=True,
            block_type="deployment",
            title="Deployment options",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "options": [
                        {"icon": "☁️", "title": "Baserow Cloud", "description": ""},
                        {"icon": "🖥️", "title": "Self-hosted (on-premise)", "description": "Own your data infrastructure at scale"},
                        {"icon": "🔒", "title": "Managed private instance", "description": "Available on request"},
                    ]
                }
            ),
        ),
        # 5 ─ AI Assistant
        dict(
            order=5,
            locale=EN,
            enabled=True,
            block_type="section_image",
            title="Tell Baserow what you need — it builds it for you",
            subtitle="Meet Kuma, your AI assistant. Describe which data you need to manage and let Kuma build it for you.",
            body="",
            image_url="",
            primary_cta_label="Learn about Kuma",
            primary_cta_url="#",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items({}),
        ),
        # 6 ─ How It Works
        dict(
            order=6,
            locale=EN,
            enabled=True,
            block_type="how_it_works",
            title="How It Works",
            subtitle="Bring in your data from spreadsheets or tools, and manage it all in one place. Automate workflows, connect integrations and build apps without coding.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "columns": [
                        {
                            "title": "Data sources",
                            "items": [
                                {"icon": "🔧", "title": "Your tools", "description": "", "tags": []},
                                {"icon": "🌐", "title": "External data sources", "description": "", "tags": ["CSV", "XML", "JSON"]},
                            ],
                        },
                        {
                            "title": "Workflows",
                            "items": [
                                {"icon": "⚡", "title": "Native automations", "description": "Automation builder", "tags": ["HTTP", "Email", "Webhooks"]},
                                {"icon": "🔗", "title": "Third-party", "description": "", "tags": []},
                            ],
                        },
                        {
                            "title": "Intuitive interfaces",
                            "items": [
                                {"icon": "📊", "title": "Databases", "description": "Visualize and collaborate", "tags": ["Grid", "Kanban", "Calendar", "Form"]},
                                {"icon": "📱", "title": "Applications", "description": "Build apps without code", "tags": []},
                                {"icon": "🤖", "title": "AI + agents", "description": "Add AI to your workflows", "tags": ["AI Field", "MCP Server"]},
                            ],
                        },
                    ]
                }
            ),
        ),
        # 7 ─ Build custom apps
        dict(
            order=7,
            locale=EN,
            enabled=True,
            block_type="section_image",
            title="Build custom applications for your specific use case",
            subtitle="Compose pages, dashboards and workflows on top of your data — without writing code.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "sidebar": [
                        {"icon": "📋", "label": "Risk Management"},
                        {"icon": "✅", "label": "Task Management"},
                        {"icon": "📈", "label": "ESG"},
                        {"icon": "📣", "label": "Marketing"},
                        {"icon": "👥", "label": "CRM"},
                        {"icon": "🛒", "label": "Purchasing"},
                        {"icon": "🏭", "label": "Manufacturing"},
                    ]
                }
            ),
        ),
        # 8 ─ Automations
        dict(
            order=8,
            locale=EN,
            enabled=True,
            block_type="automations",
            title="Automate workflows to eliminate manual work and errors",
            subtitle="Streamline tasks with no-code workflows, customizable for your needs.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"icon": "🔀", "title": "Visual logic", "description": "With triggers, branches, conditions and loops"},
                        {"icon": "🔌", "title": "Seamless integrations", "description": "Native actions (HTTP, email, webhooks) and third-party connectors"},
                        {"icon": "📝", "title": "Audit-ready logs", "description": "Meet compliance requirements"},
                    ]
                }
            ),
        ),
        # 9 ─ Dashboards
        dict(
            order=9,
            locale=EN,
            enabled=True,
            block_type="section_image",
            title="Visualize your data with dashboards",
            subtitle="Create charts to track progress and communicate to your management.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items({}),
        ),
        # 10 ─ Templates
        dict(
            order=10,
            locale=EN,
            enabled=True,
            block_type="templates_grid",
            title="Solutions templates ready to use",
            subtitle="Transform spreadsheets into custom tools.",
            body="",
            image_url="",
            primary_cta_label="Explore all solutions",
            primary_cta_url="#",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"title": "Task Management", "icon": "✅", "image": "", "url": "#"},
                        {"title": "Project Management", "icon": "📊", "image": "", "url": "#"},
                        {"title": "Risk Assessment and Management", "icon": "⚠️", "image": "", "url": "#"},
                        {"title": "Advertising Campaigns", "icon": "📣", "image": "", "url": "#"},
                        {"title": "ESG Management", "icon": "🌱", "image": "", "url": "#"},
                        {"title": "GEMBA Walks", "icon": "🏭", "image": "", "url": "#"},
                    ]
                }
            ),
        ),
        # 11 ─ Why Baserow
        dict(
            order=11,
            locale=EN,
            enabled=True,
            block_type="features_grid",
            title="Why Baserow?",
            subtitle="An open source platform with great flexibility, ease of use, security and best value for money.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {"icon_emoji": "📊", "title": "Replace spreadsheets", "description": "Manage data across teams in real time"},
                        {"icon_emoji": "💻", "title": "Custom software", "description": "Develop business apps faster and cheaper"},
                        {"icon_emoji": "🔒", "title": "Governance & compliance", "description": "Data governance & security compliance"},
                        {"icon_emoji": "☁️", "title": "Cloud or self-hosted", "description": "Security and scalability"},
                        {"icon_emoji": "📖", "title": "Open source", "description": "No vendor lock-in for business continuity"},
                        {"icon_emoji": "💰", "title": "Best value", "description": "Manage costs at any scale"},
                    ]
                }
            ),
        ),
        # 12 ─ Comparison
        dict(
            order=12,
            locale=EN,
            enabled=True,
            block_type="comparison",
            title="The open source Airtable alternative",
            subtitle="Get everything you enjoy about Airtable, with none of the downsides.",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "our_name": "Baserow",
                    "competitor": "Airtable",
                    "items": [
                        {"feature": "Open source", "us": True, "us_text": "Open source", "them": False, "them_text": "Closed source"},
                        {"feature": "Cloud + self-hosted", "us": True, "us_text": "Cloud + self-hosted deployments", "them": False, "them_text": "No self-hosting"},
                        {"feature": "Competitive pricing", "us": True, "us_text": "Competitive pricing", "them": False, "them_text": "More expensive"},
                        {"feature": "Unlimited scalability", "us": True, "us_text": "Unlimited scalability (self-hosted)", "them": False, "them_text": "Low row limits, even at the enterprise level"},
                        {"feature": "API-first", "us": True, "us_text": "API-first makes every feature an integration endpoint for automation", "them": False, "them_text": "Limiting API"},
                        {"feature": "Customize and extend", "us": True, "us_text": "Customize and extend with both frontend and backend plugins", "them": False, "them_text": "Only offers frontend plugin extensions"},
                        {"feature": "Fast and stable", "us": True, "us_text": "Fast and more stable, even at scale", "them": False, "them_text": ""},
                        {"feature": "GDPR, HIPAA, SOC 2", "us": True, "us_text": "GDPR, HIPAA, and SOC 2 compliant", "them": False, "them_text": ""},
                        {"feature": "Application Builder", "us": True, "us_text": "Powerful Application Builder", "them": False, "them_text": ""},
                    ],
                }
            ),
        ),
        # 13 ─ Testimonials
        dict(
            order=13,
            locale=EN,
            enabled=True,
            block_type="testimonials",
            title="Enterprise-ready for all teams and industries",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "items": [
                        {
                            "quote": "We love the speed of deployment and simplicity of the platform.",
                            "name": "Cathy Tondu",
                            "role": "Digital Product Manager",
                            "logo": "",
                            "avatar": "",
                        },
                        {
                            "quote": "We use Baserow as the single source of truth for policy and risk incident data. We like the simplicity, flexibility, and security it provides.",
                            "name": "David Porter",
                            "role": "Vice President, Group Risk Management",
                            "logo": "",
                            "avatar": "",
                        },
                        {
                            "quote": "Baserow is a key technology partner for our real estate agents' all-in-one operational platform.",
                            "name": "Bryn Humble",
                            "role": "Chief Product Officer",
                            "logo": "",
                            "avatar": "",
                        },
                    ]
                }
            ),
        ),
        # 14 ─ CTA
        dict(
            order=14,
            locale=EN,
            enabled=True,
            block_type="cta",
            title="Ready to gain control over your data?",
            subtitle="Start your journey with Baserow today.",
            body="",
            image_url="",
            primary_cta_label="Sign up for free",
            primary_cta_url="/signup",
            secondary_cta_label="Contact sales",
            secondary_cta_url="/login",
            extra_data=_items({"dark": True}),
        ),
        # 15 ─ Footer
        dict(
            order=15,
            locale=EN,
            enabled=True,
            block_type="footer",
            title="",
            subtitle="",
            body="",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
            extra_data=_items(
                {
                    "columns": [
                        {
                            "title": "Company",
                            "links": [
                                {"label": "Jobs", "url": "#"},
                                {"label": "FAQ", "url": "#"},
                                {"label": "Partners", "url": "#"},
                                {"label": "Contact", "url": "#"},
                                {"label": "Status", "url": "#"},
                            ],
                        },
                        {
                            "title": "Platform",
                            "links": [
                                {"label": "Templates", "url": "#"},
                                {"label": "Pricing", "url": "#"},
                                {"label": "Community", "url": "#"},
                                {"label": "Knowledge base", "url": "#"},
                                {"label": "All integrations", "url": "#"},
                            ],
                        },
                        {
                            "title": "Blog",
                            "links": [
                                {"label": "Baserow release notes", "url": "#"},
                                {"label": "Airtable vs. Baserow", "url": "#"},
                                {"label": "Open-source software: top alternatives", "url": "#"},
                            ],
                        },
                        {
                            "title": "For developers",
                            "links": [
                                {"label": "Documentation", "url": "#"},
                                {"label": "API", "url": "#"},
                                {"label": "OpenAPI", "url": "#"},
                            ],
                        },
                    ],
                    "newsletter": {
                        "title": "Join our newsletter",
                        "description": "Stay up to date with the latest developments and releases by signing up for our newsletter.",
                        "placeholder": "Your email address",
                        "button": "Subscribe",
                    },
                    "copyright": "© 2026 Baserow. All rights reserved.",
                    "legal_links": [
                        {"label": "Terms & conditions", "url": "#"},
                        {"label": "Privacy policy", "url": "#"},
                    ],
                    "social_links": [],
                }
            ),
        ),
    ]

    for row in ru_blocks + en_blocks:
        LandingBlock.objects.create(**row)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0116_landingblock_extra_data"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
