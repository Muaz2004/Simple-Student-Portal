fetch('/news/')
  .then(response => response.json())
  .then(data => {
    console.log(data);
    const container = document.getElementById('news-container');

    data.forEach(item => {
      const newsItem = document.createElement('div');
      newsItem.style.border = '1px solid #ddd';
      newsItem.style.padding = '12px';
      newsItem.style.marginBottom = '20px';
      newsItem.style.borderRadius = '10px';
      newsItem.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';

      const topic = document.createElement('h3');
      topic.textContent = item.topic;

      const message = document.createElement('p');
      message.textContent = item.message;

      const image = document.createElement('img');
      image.src = item.image;
      image.alt = 'Image';
      image.style.width = '100%';
      image.style.maxWidth = '400px';
      image.style.marginTop = '10px';
      image.style.borderRadius = '6px';

      newsItem.appendChild(topic);   // ✅ was previously announcement, which doesn't exist
      newsItem.appendChild(message);

      if (item.image) {
        newsItem.appendChild(image);
      }

      container.appendChild(newsItem);
    });
  });
