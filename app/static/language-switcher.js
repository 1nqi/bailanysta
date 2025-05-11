// Объект с переводами
const translations = {
    'ru': {
        'home': 'Bailanysta',
        'profile_list': 'Список профилей',
        'logout': 'Выход',
        'register': 'Регистрация',
        'login': 'Вход',
        'search': 'Поиск',
        'dark_theme': 'Темная тема',
        'light_theme': 'Светлая тема',
        'language': 'Язык',
        'create_khabar': 'Создать хабар',
        'post_khabar': 'Опубликовать хабар',
        'generate_ai': 'Сгенерировать с помощью ИИ',
        'profile': 'Профиль',
        'follow': 'Подписаться',
        'unfollow': 'Отписаться',
        'follows': 'Подписки',
        'followers': 'Подписчики',
        'edit': 'Редактировать',
        'delete': 'Удалить',
        'like': 'Нравится',
        'unlike': 'Не нравится',
        'comment': 'Комментарий',
        'post_comment': 'Опубликовать комментарий',
        'edit_profile': 'Редактировать профиль',
        'update_profile': 'Обновить профиль',
        'bio': 'О себе',
        'website': 'Веб-сайт',
        'social_links': 'Социальные сети'
    },
    'en': {
        'home': 'Bailanysta',
        'profile_list': 'Profile List',
        'logout': 'Logout',
        'register': 'Register',
        'login': 'Login',
        'search': 'Search',
        'dark_theme': 'Dark Theme',
        'light_theme': 'Light Theme',
        'language': 'Language',
        'create_khabar': 'Create khabar',
        'post_khabar': 'Post khabar',
        'generate_ai': 'Generate with AI',
        'profile': 'Profile',
        'follow': 'Follow',
        'unfollow': 'Unfollow',
        'follows': 'Follows',
        'followers': 'Followers',
        'edit': 'Edit',
        'delete': 'Delete',
        'like': 'Like',
        'unlike': 'Unlike',
        'comment': 'Comment',
        'post_comment': 'Post comment',
        'edit_profile': 'Edit Profile',
        'update_profile': 'Update Profile',
        'bio': 'Bio',
        'website': 'Website',
        'social_links': 'Social Links'
    },
    'kk': {
        'home': 'Bailanysta',
        'profile_list': 'Профильдер тізімі',
        'logout': 'Шығу',
        'register': 'Тіркелу',
        'login': 'Кіру',
        'search': 'Іздеу',
        'dark_theme': 'Қараңғы тақырып',
        'light_theme': 'Ашық тақырып',
        'language': 'Тіл',
        'create_khabar': 'Хабар құру',
        'post_khabar': 'Хабарландыру',
        'generate_ai': 'Жасанды интеллектпен жасау',
        'profile': 'Профиль',
        'follow': 'Жазылу',
        'unfollow': 'Жазылудан бас тарту',
        'follows': 'Жазылымдар',
        'followers': 'Жазылушылар',
        'edit': 'Өңдеу',
        'delete': 'Жою',
        'like': 'Ұнайды',
        'unlike': 'Ұнбайды',
        'comment': 'Пікір',
        'post_comment': 'Пікір қосу',
        'edit_profile': 'Профильді өңдеу',
        'update_profile': 'Профильді жаңарту',
        'bio': 'Өзі туралы',
        'website': 'Веб-сайт',
        'social_links': 'Әлеуметтік желілер'
    }
};

// Функция для установки языка
function setLanguage(lang) {
    localStorage.setItem('language', lang);
    updateContent(lang);
    updateLanguageButton(lang);
}

// Функция для обновления контента на странице
function updateContent(lang) {
    const elements = document.querySelectorAll('[data-translate]');
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
}

// Функция для обновления текста кнопки выбора языка
function updateLanguageButton(lang) {
    const btn = document.getElementById('language-btn');
    if (btn) {
        btn.textContent = translations[lang]['language'];
    }
}

// Функция для переключения языка
function toggleLanguage() {
    const currentLang = localStorage.getItem('language') || 'ru';
    const languages = ['ru', 'en', 'kk'];
    const currentIndex = languages.indexOf(currentLang);
    const nextIndex = (currentIndex + 1) % languages.length;
    setLanguage(languages[nextIndex]);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('language') || 'ru';
    setLanguage(savedLang);
}); 