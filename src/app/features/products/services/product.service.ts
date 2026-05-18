import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ProductPreview } from '../models/product-preview';
import { environment } from '../../../env/enviroment';
import { Product } from '../models/product';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  api_url = environment.apiUrl + '/productos';

  constructor(private http: HttpClient) { }

  getProducts() {
    return this.http.get<ProductsResponse>(this.api_url);
  }

  getProductById(id: number) {
    return this.http
              .get<{product: Product}>(`${this.api_url}/${id}`)
              .pipe( map(response => response.product) )
              ;
  }
}

export interface ProductsResponse {
  products: ProductPreview[];
}
