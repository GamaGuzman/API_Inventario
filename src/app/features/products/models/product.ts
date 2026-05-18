
export interface Product {
  id: number;
  titulo: string;
  descripcion: string;
  precio: number;
  moneda: string;
  imagen_url: string;
  stock: number;
  rating_promedio?: number;
}
