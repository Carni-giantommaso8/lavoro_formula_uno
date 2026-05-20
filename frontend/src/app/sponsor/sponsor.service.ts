import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SponsorService {
  private apiUrl = 'https://reimagined-dollop-q7pjjg4gwww6fx5v-5000.app.github.dev/api/sponsor';

  constructor(private http: HttpClient) { }

  getSponsors() {
    return this.http.get(this.apiUrl);
  }

  deleteSponsor(id: number){
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  addSponsor(nuovoSponsor: any){
    return this.http.post(this.apiUrl, nuovoSponsor)
  }

  updateSponsor(id: number, sponsorAggiornato: any){
    return this.http.put(`${this.apiUrl}/${id}`, sponsorAggiornato);
  }
}