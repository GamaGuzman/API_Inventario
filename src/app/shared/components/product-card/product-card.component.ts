import { Component, Input } from '@angular/core';
import { ProductPreview } from '../../../features/products/models/product-preview';
import { RouterLink } from '@angular/router';
import { NgClass } from '@angular/common';

@Component({
  selector: 'app-product-card',
  imports: [RouterLink, NgClass],
  templateUrl: './product-card.component.html',
  styleUrl: './product-card.component.css'
})
export class ProductCardComponent {

  @Input() product : ProductPreview | null = null;
}
