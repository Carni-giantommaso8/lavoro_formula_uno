import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PilotiService {
  private apiUrl = 'https://reimagined-dollop-q7pjjg4gwww6fx5v-5000.app.github.dev/api/piloti';
  private scuderieUrl = 'https://reimagined-dollop-q7pjjg4gwww6fx5v-5000.app.github.dev/api/scuderie';
  private macchineUrl = 'https://reimagined-dollop-q7pjjg4gwww6fx5v-5000.app.github.dev/api/macchine';
  constructor(private http: HttpClient) { }

  getPiloti() {
    return this.http.get(this.apiUrl);
  }

  getScuderie() {
    return this.http.get(this.scuderieUrl);
  }

  deletePilota(id: number) {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  addPilota(nuovoPilota: any) {
    return this.http.post(this.apiUrl, nuovoPilota);
  }

  updatePilota(id: number, datiAggiornati: any) {
    return this.http.put(`${this.apiUrl}/${id}`, datiAggiornati);
  }
  getPilotaById(id: number) {
  return this.http.get(`${this.apiUrl}/${id}`);
}

getMacchinaByScuderia(idScuderia: number) {
  return this.http.get(`${this.macchineUrl}/scuderia/${idScuderia}`);
}
}