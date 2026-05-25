import { Component, OnInit, signal } from '@angular/core';
import { CircuitiService } from './circuiti.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-circuiti',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './circuiti.html',
  styleUrl: './circuiti.css'
})
export class CircuitiComponent implements OnInit {
  circuiti = signal<any[]>([]);
  mostraForm = signal(false);
  circuitoInModifica = signal<number | null>(null);

  tipiCircuito = ['Cittadino', 'Permanente', 'Ibrido'];

  nuovoCircuito = {
    nome: '',
    localita: '',
    nazione: '',
    lunghezza_km: null as number | null,
    numero_curve: null as number | null,
    record_sul_giro: '',
    capacita_spettatori: null as number | null,
    tipo_circuito: 'Permanente'
  };

  constructor(private service: CircuitiService) {}

  ngOnInit() { this.caricaCircuiti(); }

  caricaCircuiti() {
    this.service.getCircuiti().subscribe((dati: any) => this.circuiti.set(dati));
  }

  avviaModifica(c: any) {
    this.circuitoInModifica.set(c.id);
    this.nuovoCircuito = {
      nome: c.nome,
      localita: c.localita,
      nazione: c.nazione,
      lunghezza_km: c.lunghezza_km,
      numero_curve: c.numero_curve,
      record_sul_giro: c.record_sul_giro,
      capacita_spettatori: c.capacita_spettatori,
      tipo_circuito: c.tipo_circuito
    };
    this.mostraForm.set(true);
  }

  annullaForm() {
    this.mostraForm.set(false);
    this.circuitoInModifica.set(null);
    this.nuovoCircuito = {
      nome: '', localita: '', nazione: '', lunghezza_km: null,
      numero_curve: null, record_sul_giro: '', capacita_spettatori: null, tipo_circuito: 'Permanente'
    };
  }

  salvaCircuito() {
    const id = this.circuitoInModifica();
    const obs = id
      ? this.service.updateCircuito(id, this.nuovoCircuito)
      : this.service.addCircuito(this.nuovoCircuito);
    obs.subscribe(() => { this.caricaCircuiti(); this.annullaForm(); });
  }

  elimina(id: number) {
    if (confirm('Sei sicuro di voler eliminare questo circuito? Verranno eliminati anche i Gran Premi collegati.')) {
      this.service.deleteCircuito(id).subscribe(() => this.caricaCircuiti());
    }
  }

  badgeColor(tipo: string): string {
    switch (tipo) {
      case 'Cittadino':  return 'bg-warning text-dark';
      case 'Permanente': return 'bg-success';
      case 'Ibrido':     return 'bg-info text-dark';
      default:           return 'bg-secondary';
    }
  }
}