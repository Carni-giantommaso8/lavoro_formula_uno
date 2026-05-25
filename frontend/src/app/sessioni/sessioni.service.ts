import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class SessioniService {
  private base = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api/sessioni';

  constructor(private http: HttpClient) {}

  getSessioni(idGp?: number) {
    const url = idGp ? `${this.base}?id_gran_premio=${idGp}` : this.base;
    return this.http.get<any[]>(url);
  }
  addSessione(d: any)    { return this.http.post(this.base, d); }
  updateSessione(id: number, d: any) { return this.http.put(`${this.base}/${id}`, d); }
  deleteSessione(id: number)         { return this.http.delete(`${this.base}/${id}`); }
}