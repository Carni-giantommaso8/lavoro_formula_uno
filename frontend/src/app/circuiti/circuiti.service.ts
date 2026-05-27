import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CircuitiService {
  private apiUrl = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api/circuiti';

  constructor(private http: HttpClient) {}

  getCircuiti() {
    return this.http.get(this.apiUrl);
  }

  addCircuito(circuito: any) {
    return this.http.post(this.apiUrl, circuito);
  }

  updateCircuito(id: number, circuito: any) {
    return this.http.put(`${this.apiUrl}/${id}`, circuito);
  }

  deleteCircuito(id: number) {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}