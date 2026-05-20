import { Component, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PilotiService } from './piloti.service';

@Component({
  selector: 'app-piloti',
  imports: [CommonModule, FormsModule],
  templateUrl: './piloti.html',
  styleUrl: './piloti.css'
})
export class PilotiComponent implements OnInit {
  piloti = signal<any[]>([]);
  scuderie = signal<any[]>([]);
  mostraForm = signal(false);
  pilotaInModifica = signal<any>(null);

  nuovoPilota: any = {
    nome: '',
    cognome: '',
    data_nascita: '',
    nazionalita: '',
    numero_gara: null,
    stipendio_annuo: null,
    id_scuderia: null
  };

  constructor(private pilotiService: PilotiService) {}

  ngOnInit() {
    this.caricaPiloti();
    this.caricaScuderie();
  }

  caricaPiloti() {
    this.pilotiService.getPiloti().subscribe((data: any) => {
      this.piloti.set(data);
    });
  }

  caricaScuderie() {
    this.pilotiService.getScuderie().subscribe((data: any) => {
      this.scuderie.set(data);
    });
  }

  salvaPilota() {
    if (this.pilotaInModifica()) {
      this.pilotiService.updatePilota(this.pilotaInModifica().id, this.nuovoPilota).subscribe(() => {
        this.caricaPiloti();
        this.annullaForm();
      });
    } else {
      this.pilotiService.addPilota(this.nuovoPilota).subscribe(() => {
        this.caricaPiloti();
        this.annullaForm();
      });
    }
  }

  avviaModifica(p: any) {
    this.pilotaInModifica.set(p);
    this.nuovoPilota = { ...p };
    this.mostraForm.set(true);
  }

  annullaForm() {
    this.pilotaInModifica.set(null);
    this.nuovoPilota = {
      nome: '',
      cognome: '',
      data_nascita: '',
      nazionalita: '',
      numero_gara: null,
      stipendio_annuo: null,
      id_scuderia: null
    };
    this.mostraForm.set(false);
  }

  elimina(id: number) {
    this.pilotiService.deletePilota(id).subscribe(() => {
      this.caricaPiloti();
    });
  }
}