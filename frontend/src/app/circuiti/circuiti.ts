import { Component, signal, OnInit, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CircuitiService } from './circuiti.service';

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
  circuitoInModifica = signal<any>(null);
  modalAperto = signal(false);
  circuitoSelezionato = signal<any>(null);
  filtroTipo = signal<string>('Tutti');

  circuitiFiltrati = computed(() => {
    if (this.filtroTipo() === 'Tutti') return this.circuiti();
    return this.circuiti().filter(c => c.tipo_circuito === this.filtroTipo());
  });

  nuovoCircuito: any = {
    nome: '', localita: '', nazione: '', lunghezza_km: null,
    numero_curve: null, record_sul_giro: '', capacita_spettatori: null, tipo_circuito: null
  };

  private fotoCircuitiMap: Record<string, string> = {
  'Albert Park Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.png',
  'Shanghai International Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/China_Circuit.png',
  'Suzuka Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.png',
  'Miami International Autodrome': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.png',
  'Circuit Gilles Villeneuve': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Canada_Circuit.png',
  'Circuit de Monaco': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monaco_Circuit.png',
  'Circuit de Barcelona-Catalunya': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.png',
  'Red Bull Ring': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit.png',
  'Silverstone Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit.png',
  'Circuit de Spa-Francorchamps': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.png',
  'Hungaroring': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Hungary_Circuit.png',
  'Circuit Zandvoort': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Netherlands_Circuit.png',
  'Autodromo Nazionale Monza': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Italy_Circuit.png',
  'Circuito de Madrid': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.png',
  'Baku City Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Baku_Circuit.png',
  'Marina Bay Street Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Singapore_Circuit.png',
  'Circuit of the Americas': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.png',
  'Autodromo Hermanos Rodriguez': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit.png',
  'Autodromo Jose Carlos Pace': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit.png',
  'Las Vegas Strip Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Las_Vegas_Circuit.png',
  'Lusail International Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Qatar_Circuit.png',
  'Yas Marina Circuit': 'https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit.png',
};
  constructor(private circuitiService: CircuitiService) {}

  ngOnInit() {
    this.caricaCircuiti();
  }

  caricaCircuiti() {
    this.circuitiService.getCircuiti().subscribe((data: any) => this.circuiti.set(data));
  }

  getFotoCircuito(nome: string): string {
    return this.fotoCircuitiMap[nome] || '';
  }

  apriDettaglio(c: any) {
    this.circuitoSelezionato.set(c);
    this.modalAperto.set(true);
    document.body.style.overflow = 'hidden';
  }

  chiudiModal() {
    this.modalAperto.set(false);
    document.body.style.overflow = '';
  }

  avviaModifica(c: any) {
    this.circuitoInModifica.set(c);
    this.nuovoCircuito = { ...c };
    this.mostraForm.set(true);
  }

  annullaForm() {
    this.circuitoInModifica.set(null);
    this.nuovoCircuito = {
      nome: '', localita: '', nazione: '', lunghezza_km: null,
      numero_curve: null, record_sul_giro: '', capacita_spettatori: null, tipo_circuito: null
    };
    this.mostraForm.set(false);
  }

  salvaCircuito() {
    if (this.circuitoInModifica()) {
      this.circuitiService.updateCircuito(this.circuitoInModifica().id, this.nuovoCircuito).subscribe(() => {
        this.caricaCircuiti(); this.annullaForm();
      });
    } else {
      this.circuitiService.addCircuito(this.nuovoCircuito).subscribe(() => {
        this.caricaCircuiti(); this.annullaForm();
      });
    }
  }

  elimina(id: number) {
    if (confirm('Eliminare questo circuito?')) {
      this.circuitiService.deleteCircuito(id).subscribe(() => this.caricaCircuiti());
    }
  }

  getTipoBadgeClass(tipo: string): string {
    switch (tipo) {
      case 'Cittadino': return 'bg-warning text-dark';
      case 'Permanente': return 'bg-success';
      case 'Ibrido': return 'bg-info text-dark';
      default: return 'bg-secondary';
    }
  }
}