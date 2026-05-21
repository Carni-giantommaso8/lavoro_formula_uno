import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ClassificaService {
  private baseUrl = 'https://reimagined-dollop-q7pjjg4gwww6fx5v-5000.app.github.dev/api/classifica';

  constructor(private http: HttpClient) { }

  getClassificaPiloti() {
    return this.http.get(`${this.baseUrl}/piloti`);
  }

  getClassificaCostruttori() {
    return this.http.get(`${this.baseUrl}/costruttori`);
  }
}