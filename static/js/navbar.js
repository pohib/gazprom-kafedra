// функция для
document.addEventListener('DOMContentLoaded', function () {
    const burgerMenu = document.querySelector('.burger-menu');
    const navMenu = document.querySelector('.nav-menu');

    burgerMenu.addEventListener('click', function () {
        navMenu.classList.toggle('active');
    });
});

// функция для получения статистики просмотров
function viewStats() {
    return {
        stats: {dayViews: 0, weekViews: 0, monthViews: 0},
        async fetchStats() {
            try {
                const response = await fetch('/api/stats', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin' // Для отправки куки вместе с запросом
                });
                this.stats = await response.json();
            } catch (error) {
                console.error('Ошибка при получении статистики просмотров:', error);
            }
        }
    }
}


