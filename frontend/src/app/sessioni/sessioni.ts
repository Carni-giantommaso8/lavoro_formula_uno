import { Component, OnInit, signal } from '@angular/core';
import { SessioniService } from './sessioni.service';
import { GranPremiService } from '../gran-premi/gran-premi.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-sessioni',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './sessioni.html',
  styleUrl: './sessioni.css'
})
export class SessioniComponent implements OnInit {
  sessioni = signal<any[]>([]);
  granPremi = signal<any[]>([]);
  mostraForm = signal(false);
  sessioneInModifica = signal<number | null>(null);

  tipiSessione = ['FP1', 'FP2', 'FP3', 'Qualifiche', 'Sprint', 'Gara'];
  filtroGP = signal<number | null>(null);

  nuovaSessione = {
    tipo: 'Gara',
    orario_inizio: '',
    id_gran_premio: null as number | null
  };

  constructor(
    private service: SessioniService,
    private gpService: GranPremiService
  ) {}

  ngOnInit() {
    this.caricaSessioni();
    this.gpService.getGranPremi().subscribe((d: any) => this.granPremi.set(d));
  }

  caricaSessioni() {
    const idGp = this.filtroGP();
    this.service.getSessioni(idGp ?? undefined).subscribe((d: any) => this.sessioni.set(d));
  }

  applicaFiltro(idGp: string) {
    this.filtroGP.set(idGp ? +idGp : null);
    this.caricaSessioni();
  }

  avviaModifica(s: any) {
    this.sessioneInModifica.set(s.id);
    const dt = s.orario_inizio ? s.orario_inizio.replace(' ', 'T').substring(0, 16) : '';
    this.nuovaSessione = {
      tipo: s.tipo,
      orario_inizio: dt,
      id_gran_premio: s.id_gran_premio
    };
    this.mostraForm.set(true);
  }

  annullaForm() {
    this.mostraForm.set(false);
    this.sessioneInModifica.set(null);
    this.nuovaSessione = { tipo: 'Gara', orario_inizio: '', id_gran_premio: null };
  }

  salvaSessione() {
    const id = this.sessioneInModifica();
    const payload = {
      ...this.nuovaSessione,
      orario_inizio: this.nuovaSessione.orario_inizio.replace('T', ' ')
    };
    const obs = id
      ? this.service.updateSessione(id, payload)
      : this.service.addSessione(payload);
    obs.subscribe(() => { this.caricaSessioni(); this.annullaForm(); });
  }

  elimina(id: number) {
    if (confirm('Eliminare questa sessione? Verranno eliminati anche i risultati collegati.')) {
      this.service.deleteSessione(id).subscribe(() => this.caricaSessioni());
    }
  }

  badgeTipo(tipo: string): string {
    switch (tipo) {
      case 'Gara':       return 'bg-danger';
      case 'Qualifiche': return 'bg-warning text-dark';
      case 'Sprint':     return 'bg-primary';
      case 'FP1': case 'FP2': case 'FP3': return 'bg-secondary';
      default:           return 'bg-dark';
    }
  }
}