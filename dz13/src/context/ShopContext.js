import React, { createContext, useMemo, useCallback } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

export const ShopContext = createContext();

export const ShopProvider = ({ children }) => {
  const [favorites, setFavorites] = useLocalStorage('favorites', []);

  const addToFavorites = useCallback((product) => {
    setFavorites(prev => [...prev, product]);
  }, [setFavorites]);

  const removeFromFavorites = useCallback((productId) => {
    setFavorites(prev => prev.filter(item => item.id !== productId));
  }, [setFavorites]);

  const value = useMemo(() => ({
    favorites,
    addToFavorites,
    removeFromFavorites
  }), [favorites, addToFavorites, removeFromFavorites]);

  return (
    <ShopContext.Provider value={value}>
      {children}
    </ShopContext.Provider>
  );
};
