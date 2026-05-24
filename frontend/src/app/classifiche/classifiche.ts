import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClassificheService } from './classifiche.service';

@Component({
  selector: 'app-classifiche',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './classifiche.html',
  styleUrl: './classifiche.css'
})
export class ClassificheComponent implements OnInit {
  piloti = signal<any[]>([]);
  costruttori = signal<any[]>([]);
  vistaAttiva = signal<'piloti' | 'costruttori'>('piloti');
  includiSprint = signal<boolean>(true);
  loading = signal<boolean>(false);
  errore = signal<string>('');

  constructor(private service: ClassificheService) {}

  ngOnInit() {
    this.caricaClassifiche();
  }

  caricaClassifiche() {
    this.loading.set(true);
    this.errore.set('');

    this.service.getClassificaPiloti(this.includiSprint()).subscribe({
      next: (dati: any) => {
        this.piloti.set(dati);
        this.loading.set(false);
      },
      error: () => {
        this.errore.set('Errore nel caricamento piloti');
        this.loading.set(false);
      }
    });

    this.service.getClassificaCostruttori(this.includiSprint()).subscribe({
      next: (dati: any) => {
        this.costruttori.set(dati);
      },
      error: () => {
        this.errore.set('Errore nel caricamento costruttori');
      }
    });
  }

  toggleSprint() {
    this.includiSprint.set(!this.includiSprint());
    this.caricaClassifiche();
  }

  setVista(vista: 'piloti' | 'costruttori') {
    this.vistaAttiva.set(vista);
  }

  getScuderiaColore(scuderia: string): string {
    const colori: { [key: string]: string } = {
      'Ferrari': '#E8002D',
      'Mercedes-AMG Petronas': '#27F4D2',
      'McLaren': '#FF8000',
      'Red Bull Racing': '#3671C6',
      'Alpine': '#FF87BC',
      'Haas F1 Team': '#B6BABD',
      'Racing Bulls': '#6692FF',
      'Williams Racing': '#64C4FF',
      'Audi': '#D0D3D4',
      'Cadillac': '#00594F',
      'Aston Martin Aramco': '#229971'
    };
    return colori[scuderia] || '#ffffff';
  }
}