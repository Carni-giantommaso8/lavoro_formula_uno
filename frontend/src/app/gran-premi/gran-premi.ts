import { Component, OnInit, signal } from '@angular/core';
import { GranPremiService } from './gran-premi.service';
import { CircuitiService } from '../circuiti/circuiti.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-gran-premi',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './gran-premi.html',
  styleUrl: './gran-premi.css'
})
export class GranPremiComponent implements OnInit {
  granPremi = signal<any[]>([]);
  circuiti = signal<any[]>([]);
  mostraForm = signal(false);
  gpInModifica = signal<number | null>(null);

  nuovoGP = {
    nome_evento: '',
    edizione_numero: null as number | null,
    data_inizio: '',
    meteo_previsto: '',
    id_circuito: null as number | null
  };

  constructor(
    private service: GranPremiService,
    private circuitiService: CircuitiService
  ) {}

  ngOnInit() {
    this.caricaGranPremi();
    this.circuitiService.getCircuiti().subscribe((d: any) => this.circuiti.set(d));
  }

  caricaGranPremi() {
    this.service.getGranPremi().subscribe((dati: any) => this.granPremi.set(dati));
  }

  avviaModifica(gp: any) {
    this.gpInModifica.set(gp.id);
    this.nuovoGP = {
      nome_evento: gp.nome_evento,
      edizione_numero: gp.edizione_numero,
      data_inizio: gp.data_inizio ? gp.data_inizio.split('T')[0] : '',
      meteo_previsto: gp.meteo_previsto,
      id_circuito: gp.id_circuito
    };
    this.mostraForm.set(true);
  }

  annullaForm() {
    this.mostraForm.set(false);
    this.gpInModifica.set(null);
    this.nuovoGP = { nome_evento: '', edizione_numero: null, data_inizio: '', meteo_previsto: '', id_circuito: null };
  }

  salvaGP() {
    const id = this.gpInModifica();
    const obs = id
      ? this.service.updateGranPremio(id, this.nuovoGP)
      : this.service.addGranPremio(this.nuovoGP);
    obs.subscribe(() => { this.caricaGranPremi(); this.annullaForm(); });
  }

  elimina(id: number) {
    if (confirm('Eliminare questo Gran Premio? Verranno eliminate anche le sessioni e i risultati collegati.')) {
      this.service.deleteGranPremio(id).subscribe(() => this.caricaGranPremi());
    }
  }

  meteoIcon(meteo: string): string {
    if (!meteo) return '🌤️';
    const m = meteo.toLowerCase();
    if (m.includes('soleggiato') || m.includes('sereno')) return '☀️';
    if (m.includes('nuvoloso')) return '☁️';
    if (m.includes('variabile')) return '⛅';
    if (m.includes('pioggia') || m.includes('umido')) return '🌧️';
    if (m.includes('ventoso')) return '🌬️';
    if (m.includes('caldo')) return '🌡️';
    return '🌤️';
  }
}