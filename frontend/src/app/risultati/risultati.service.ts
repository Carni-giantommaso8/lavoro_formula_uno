import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class RisultatiService {
  private base = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api/risultati';

  constructor(private http: HttpClient) {}

  getRisultati(idSessione?: number) {
    const url = idSessione ? `${this.base}?id_sessione=${idSessione}` : this.base;
    return this.http.get<any[]>(url);
  }
  addRisultato(d: any)    { return this.http.post(this.base, d); }
  updateRisultato(id: number, d: any) { return this.http.put(`${this.base}/${id}`, d); }
  deleteRisultato(id: number)         { return this.http.delete(`${this.base}/${id}`); }
}