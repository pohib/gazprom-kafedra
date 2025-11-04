function newsFeed() {
    return {
        posts: [],
        isModalOpen: false,
        modalContent: {},
        showFullImage: false,
        loading: true,
        async fetchPosts() {
            try {
                const response = await fetch('/api/vk-news', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin' // Для отправки куки вместе с запросом
                });
                const data = await response.json();
                console.log('Received data:', data);
                if (data && data.response && data.response.items) {
                    this.posts = data.response.items.map(item => {
                        let image = 'https://via.placeholder.com/150'; // Placeholder image
                        if (item.attachments && item.attachments[0] && item.attachments[0].photo) {
                            let sizes = item.attachments[0].photo.sizes;
                            image = sizes[sizes.length - 1].url; // Берем наибольшее доступное изображение
                        }
                        return {
                            id: item.id,
                            title: item.text.split('\n')[0],
                            shortBody: item.text.split('\n').slice(1).join(' ').substring(0, 100) + '...',
                            body: item.text.replace(/\n/g, '<br>'), // Преобразование новых строк в HTML
                            image: image,
                            views: item.views ? item.views.count : 0,
                            date: item.date,
                            url: `https://vk.com/wall-218299724_${item.id}`
                        };
                    });
                } else {
                    console.error('Unexpected data structure:', data);
                }
            } catch (error) {
                console.error('Ошибка при получении новостей:', error);
            } finally {
                this.loading = false;
            }
        },
        openModal(post) {
            this.modalContent = {
                ...post,
                body: post.body // Полный текст новости
            };
            this.isModalOpen = true;
            document.body.style.overflow = 'hidden'; // Отключение прокрутки фона
            this.$nextTick(() => {
                if (this.$refs.modal) {
                    this.$refs.modal.focus(); // Перехват фокуса
                }
            });
        },
        closeModal() {
            this.isModalOpen = false;
            document.body.style.overflow = ''; // Включение прокрутки фона
            this.showFullImage = false;
        },
        openPhotoSwipe(imageSrc) {
            const pswpElement = document.querySelectorAll('.pswp')[0];
            const items = [
                {
                    src: imageSrc,
                    w: 1600,
                    h: 900
                }
            ];
            const options = {
                index: 0
            };
            const gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
            gallery.init();
        },
        init() {
            this.fetchPosts();
        }
    };
}
