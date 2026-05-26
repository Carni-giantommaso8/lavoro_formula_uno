import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class GranPremiService {
  private base = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api/gran_premi';

  constructor(private http: HttpClient) {}

  getGranPremi()           { return this.http.get<any[]>(this.base); }
  addGranPremio(d: any)    { return this.http.post(this.base, d); }
  updateGranPremio(id: number, d: any) { return this.http.put(`${this.base}/${id}`, d); }
  deleteGranPremio(id: number)         { return this.http.delete(`${this.base}/${id}`); }
}