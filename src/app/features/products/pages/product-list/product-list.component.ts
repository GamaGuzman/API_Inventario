import { Component } from '@angular/core';
import { ProductPreview } from '../../models/product-preview';
import { ProductService, ProductsResponse } from '../../services/product.service';
import { ProductCardComponent } from '../../../../shared/components/product-card/product-card.component';


@Component({
  selector: 'app-product-list',
  imports: [ProductCardComponent],
  templateUrl: './product-list.component.html',
  styleUrl: './product-list.component.css'
})
export class ProductListComponent {

  public products: ProductPreview[] = [];

  constructor(private productService: ProductService) { }

  ngOnInit() {
    this.productService.getProducts().subscribe(
      (data: ProductsResponse) => {
      this.products = data.products;
    }, (error) => {
      console.error('Error al pedir los productos: ', error);
    }
  );
  }
}
