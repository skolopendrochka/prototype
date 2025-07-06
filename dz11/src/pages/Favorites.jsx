import React, { memo, useContext } from 'react';
import { ShopContext } from '../context/ShopContext';
import ProductCard from '../components/ProductCard';

const Favorites = memo(() => {
  const { favorites, removeFromFavorites } = useContext(ShopContext);

  return (
    <div className="favorites-page">
      <h1>Your Favorites</h1>
      {favorites.length === 0 ? (
        <p>No favorites yet</p>
      ) : (
        <div className="products-grid">
          {favorites.map(product => (
            <ProductCard 
              key={product.id} 
              product={product}
              isFavorite={true}
              onRemove={removeFromFavorites}
            />
          ))}
        </div>
      )}
    </div>
  );
});

export default Favorites;
