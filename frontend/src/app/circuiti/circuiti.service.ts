import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class CircuitiService {
  private base = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api/circuiti';

  constructor(private http: HttpClient) {}

  getCircuiti()           { return this.http.get<any[]>(this.base); }
  addCircuito(d: any)     { return this.http.post(this.base, d); }
  updateCircuito(id: number, d: any) { return this.http.put(`${this.base}/${id}`, d); }
  deleteCircuito(id: number)         { return this.http.delete(`${this.base}/${id}`); }
}