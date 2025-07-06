// Функция для имитации запроса к API
function fetchData(url) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (url === '/users') {
        resolve([
          { id: 1, name: 'Alice' },
          { id: 2, name: 'Bob' }
        ]);
      } else if (url.startsWith('/user/')) {
        const userId = parseInt(url.split('/')[2]);
        if (userId === 1) {
          resolve({ id: 1, name: 'Alice', age: 25, email: 'alice@example.com' });
        } else {
          reject(new Error('User not found'));
        }
      } else {
        reject(new Error('Invalid URL'));
      }
    }, 2000);
  });
}

// Цепочка запросов
fetchData('/users')
  .then(users => {
    console.log('Список пользователей:', users);
    return fetchData(`/user/${users[0].id}`);
  })
  .then(user => {
    console.log('Данные первого пользователя:', user);
  })
  .catch(error => {
    console.error('Ошибка:', error.message);
  });
