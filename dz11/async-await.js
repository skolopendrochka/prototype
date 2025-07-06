// Функция задержки
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Имитация запроса к API
async function fetchData(url) {
  await delay(2000);
  
  if (url === '/users') {
    return [
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' }
    ];
  } else if (url.startsWith('/user/')) {
    const userId = parseInt(url.split('/')[2]);
    if (userId === 1) {
      return { id: 1, name: 'Alice', age: 25, email: 'alice@example.com' };
    }
    throw new Error('User not found');
  }
  throw new Error('Invalid URL');
}

// Основная функция
async function getUserData() {
  try {
    const users = await fetchData('/users');
    console.log('Список пользователей:', users);
    
    await delay(1000); // Добавляем задержку между запросами
    
    const user = await fetchData(`/user/${users[0].id}`);
    console.log('Данные первого пользователя:', user);
  } catch (error) {
    console.error('Ошибка:', error.message);
  }
}

// Вызов функции
getUserData();
