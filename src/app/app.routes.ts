import { Routes } from '@angular/router';

export const routes: Routes = [
    {
    path: '',
    loadComponent: () =>
      import('./features/products/pages/product-list/product-list.component').then(c => c.ProductListComponent)
  },
    {
    path: 'products/:id',
    loadComponent: () =>
      import('./features/products/pages/product-detail/product-detail.component').then(c => c.ProductDetailComponent)
  },
];
