import { Component, OnInit, signal } from '@angular/core';
import { RisultatiService } from './risultati.service';
import { SessioniService } from '../sessioni/sessioni.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-risultati',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './risultati.html',
  styleUrl: './risultati.css'
})
export class RisultatiComponent implements OnInit {
  risultati = signal<any[]>([]);
  sessioni = signal<any[]>([]);
  piloti = signal<any[]>([]);
  mostraForm = signal(false);
  risultatoInModifica = signal<number | null>(null);
  filtroSessione = signal<number | null>(null);
  vistaClassifica = signal(false);
  classifica = signal<any[]>([]);

  nuovoRisultato = {
    posizione_finale: null as number | null,
    punti_assegnati: null as number | null,
    giro_veloce: false,
    numero_pit_stop: null as number | null,
    id_pilota: null as number | null,
    id_sessione: null as number | null
  };

  private apiBase = 'https://stunning-eureka-gx44w5rr996727pq-5000.app.github.dev/api';

  constructor(
    private service: RisultatiService,
    private sessioniService: SessioniService,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.caricaRisultati();
    this.sessioniService.getSessioni().subscribe((d: any) => this.sessioni.set(d));
    this.http.get<any[]>(`${this.apiBase}/piloti`).subscribe(d => this.piloti.set(d));
  }

  caricaRisultati() {
    const id = this.filtroSessione();
    this.service.getRisultati(id ?? undefined).subscribe((d: any) => this.risultati.set(d));
  }

  caricaClassifica() {
    this.http.get<any[]>(`${this.apiBase}/classifica/piloti`).subscribe(d => this.classifica.set(d));
  }

  toggleVista() {
    this.vistaClassifica.set(!this.vistaClassifica());
    if (this.vistaClassifica()) this.caricaClassifica();
  }

  applicaFiltro(idSessione: string) {
    this.filtroSessione.set(idSessione ? +idSessione : null);
    this.caricaRisultati();
  }

  avviaModifica(r: any) {
    this.risultatoInModifica.set(r.id);
    this.nuovoRisultato = {
      posizione_finale: r.posizione_finale,
      punti_assegnati: r.punti_assegnati,
      giro_veloce: r.giro_veloce,
      numero_pit_stop: r.numero_pit_stop,
      id_pilota: r.id_pilota,
      id_sessione: r.id_sessione
    };
    this.mostraForm.set(true);
  }

  annullaForm() {
    this.mostraForm.set(false);
    this.risultatoInModifica.set(null);
    this.nuovoRisultato = {
      posizione_finale: null, punti_assegnati: null, giro_veloce: false,
      numero_pit_stop: null, id_pilota: null, id_sessione: null
    };
  }

  salvaRisultato() {
    const id = this.risultatoInModifica();
    const obs = id
      ? this.service.updateRisultato(id, this.nuovoRisultato)
      : this.service.addRisultato(this.nuovoRisultato);
    obs.subscribe(() => { this.caricaRisultati(); this.annullaForm(); });
  }

  elimina(id: number) {
    if (confirm('Eliminare questo risultato?')) {
      this.service.deleteRisultato(id).subscribe(() => this.caricaRisultati());
    }
  }

  posizioneLabel(pos: number): string {
    if (pos === 1) return '🥇';
    if (pos === 2) return '🥈';
    if (pos === 3) return '🥉';
    return `${pos}°`;
  }

  badgeSessione(tipo: string): string {
    switch (tipo) {
      case 'Gara':       return 'bg-danger';
      case 'Qualifiche': return 'bg-warning text-dark';
      case 'Sprint':     return 'bg-primary';
      default:           return 'bg-secondary';
    }
  }
}