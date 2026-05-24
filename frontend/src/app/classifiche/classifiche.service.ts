import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ClassificheService {
  private baseUrl = 'https://reimagined-dollop-q7pjjg4gwww6fx5v-5000.app.github.dev/api';

  constructor(private http: HttpClient) {}

  getClassificaPiloti(includiSprint: boolean) {
    const params = new HttpParams().set('sprint', includiSprint.toString());
    return this.http.get<any[]>(`${this.baseUrl}/classifiche/piloti`, { params });
  }

  getClassificaCostruttori(includiSprint: boolean) {
    const params = new HttpParams().set('sprint', includiSprint.toString());
    return this.http.get<any[]>(`${this.baseUrl}/classifiche/costruttori`, { params });
  }
}