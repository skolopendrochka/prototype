import { render, screen, fireEvent } from '@testing-library/react';
import { ShopProvider } from '../../src/context/ShopContext';
import Favorites from '../../src/pages/Favorites';

const mockFavorites = [
  { id: 1, title: 'Product 1', price: 10, image: 'image1.jpg' },
  { id: 2, title: 'Product 2', price: 20, image: 'image2.jpg' }
];

describe('Favorites Page', () => {
  it('renders empty state when no favorites', () => {
    render(
      <ShopProvider value={{ favorites: [] }}>
        <Favorites />
      </ShopProvider>
    );
    expect(screen.getByText('No favorites yet')).toBeInTheDocument();
  });

  it('renders favorite products', () => {
    render(
      <ShopProvider value={{ favorites: mockFavorites }}>
        <Favorites />
      </ShopProvider>
    );
    expect(screen.getByText('Product 1')).toBeInTheDocument();
    expect(screen.getByText('Product 2')).toBeInTheDocument();
  });

  it('calls removeFromFavorites when button clicked', () => {
    const removeMock = jest.fn();
    render(
      <ShopProvider value={{ favorites: mockFavorites, removeFromFavorites: removeMock }}>
        <Favorites />
      </ShopProvider>
    );
    
    fireEvent.click(screen.getAllByText('Remove from Favorites')[0]);
    expect(removeMock).toHaveBeenCalledWith(1);
  });
});
