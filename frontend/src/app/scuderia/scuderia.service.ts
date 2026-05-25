import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ScuderiaService {
  private apiUrl = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api/scuderie';
  private sponsorUrl = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api/sponsor';

  constructor(private http: HttpClient) { }

  getScuderie() {
    return this.http.get(this.apiUrl);
  }

  getSponsor() {
    return this.http.get(this.sponsorUrl);
  }

  deleteScuderia(id: number) {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  addScuderia(nuovaScuderia: any) {
    return this.http.post(this.apiUrl, nuovaScuderia);
  }

  updateScuderia(id: number, datiAggiornati: any) {
    return this.http.put(`${this.apiUrl}/${id}`, datiAggiornati);
  }
}