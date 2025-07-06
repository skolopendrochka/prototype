import React, { memo } from 'react';

const ProductCard = memo(({ product, isFavorite, onRemove }) => {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.title} />
      <h3>{product.title}</h3>
      <p>${product.price}</p>
      {isFavorite && (
        <button onClick={() => onRemove(product.id)}>
          Remove from Favorites
        </button>
      )}
    </div>
  );
});

export default ProductCard;
