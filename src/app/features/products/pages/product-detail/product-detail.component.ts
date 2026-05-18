import { Component, Inject } from '@angular/core';
import { Product } from '../../models/product';
import { ProductService } from '../../services/product.service';
import { ActivatedRoute } from '@angular/router';
import { LoadingComponent } from '../../../../shared/components/loading/loading.component';
import { NgClass } from '@angular/common';
import { NotFoundComponent } from '../../../../shared/components/not-found/not-found.component';


@Component({
  selector: 'app-product-detail',
  imports: [ NgClass , LoadingComponent, NotFoundComponent ],
  templateUrl: './product-detail.component.html',
  styleUrl: './product-detail.component.css',
})
export class ProductDetailComponent {

  public product?: Product;
  public loading = true;
  public notFound = false;



  constructor(
    private productService: ProductService,
    private route: ActivatedRoute,


  ) { }

  ngOnInit() {

    this.loadProduct();

  }

  private loadProduct() {
    const rawProductId = this.route.snapshot.paramMap.get('id');

    if (!rawProductId) {
      this.notFound = true;
      this.loading = false;
      return;
    }

    const productId = Number(rawProductId);

    if (!Number.isInteger(productId)) {
      this.notFound = true;
      this.loading = false;
      console.log("El ID de la ruta debe ser un número entero, noob");
      return;
    }

    this.productService.getProductById(productId).subscribe({
      next: (product) => {
        this.product = product;
        this.loading = false;
        console.log(this.product);
      },
      error: () => {
        this.notFound = true;
        this.loading = false;
      }
    });
  }

  saveInStorage() {

    const rawProductId = this.route.snapshot.paramMap.get('id');

    const id = Number(rawProductId);

  }
}
