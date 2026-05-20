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
  modalAperto = signal(false);
  pilotaSelezionato = signal<any>(null);
  macchinaSelezionata = signal<any>(null);

  // Foto ufficiali F1 per numero gara
  private fotoPilotiMap: Record<number, string> = {
    44: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png',
    16: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png',
    63: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.png',
    12: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/A/ANDANT01_Andrea_Kimi_Antonelli/andant01.png',
    4:  'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png',
    81: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.png',
    33: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png',
    6:  'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/I/ISAHAD01_Isack_Hadjar/isahad01.png',
    10: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/P/PIEGAS01_Pierre_Gasly/piegas01.png',
    43: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/F/FRACOL01_Franco_Colapinto/fracol01.png',
    31: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/E/ESTOCO01_Esteban_Ocon/estoco01.png',
    87: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/O/OLIBEA01_Oliver_Bearman/olibea01.png',
    30: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/L/LIALAW01_Liam_Lawson/lialaw01.png',
    40: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/A/ARVLIN01_Arvid_Lindblad/arvlin01.png',
    55: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.png',
    23: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.png',
    27: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/N/NICHUL01_Nico_Hulkenberg/nichul01.png',
    5:  'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/G/GABBOR01_Gabriel_Bortoleto/gabbor01.png',
    11: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.png',
    77: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/V/VALBOT01_Valtteri_Bottas/valbot01.png',
    14: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.png',
    18: 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/L/LANSTR01_Lance_Stroll/lanstr01.png',
  };

  // Foto ufficiali F1 per sigla macchina
  private fotoMacchineMap: Record<string, string> = {
    'SF-26':    'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/ferrari.png',
    'W17':      'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/mercedes.png',
    'MCL43':    'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/mclaren.png',
    'RB22':     'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/red-bull-racing.png',
    'A526':     'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/alpine.png',
    'VF-26':    'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/haas.png',
    'VCARB 02': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/rb.png',
    'FW47':     'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/williams.png',
    'C44e':     'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/kick-sauber.png',
    'CF1':      'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/haas.png',
    'AMR26':    'https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/teams/2025/aston-martin.png',
  };

  nuovoPilota: any = {
    nome: '', cognome: '', data_nascita: '', nazionalita: '',
    numero_gara: null, stipendio_annuo: null, id_scuderia: null
  };

  constructor(private pilotiService: PilotiService) {}

  ngOnInit() {
    this.caricaPiloti();
    this.caricaScuderie();
  }

  caricaPiloti() {
    this.pilotiService.getPiloti().subscribe((data: any) => this.piloti.set(data));
  }

  caricaScuderie() {
    this.pilotiService.getScuderie().subscribe((data: any) => this.scuderie.set(data));
  }

  getFotoPilota(numeroGara: number): string {
    return this.fotoPilotiMap[numeroGara] || '';
  }

  getFotoMacchina(sigla: string): string {
    return this.fotoMacchineMap[sigla] || '';
  }

  apriDettaglio(p: any) {
    this.pilotaSelezionato.set(p);
    this.macchinaSelezionata.set(null);
    if (p.id_scuderia) {
      this.pilotiService.getMacchinaByScuderia(p.id_scuderia).subscribe({
        next: (m: any) => this.macchinaSelezionata.set(m),
        error: () => {}
      });
    }
    this.modalAperto.set(true);
    document.body.style.overflow = 'hidden';
  }

  chiudiModal() {
    this.modalAperto.set(false);
    document.body.style.overflow = '';
  }

  salvaPilota() {
    if (this.pilotaInModifica()) {
      this.pilotiService.updatePilota(this.pilotaInModifica().id, this.nuovoPilota).subscribe(() => {
        this.caricaPiloti(); this.annullaForm();
      });
    } else {
      this.pilotiService.addPilota(this.nuovoPilota).subscribe(() => {
        this.caricaPiloti(); this.annullaForm();
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
    this.nuovoPilota = { nome: '', cognome: '', data_nascita: '', nazionalita: '', numero_gara: null, stipendio_annuo: null, id_scuderia: null };
    this.mostraForm.set(false);
  }

  elimina(id: number) {
    if (confirm('Eliminare questo pilota?')) {
      this.pilotiService.deletePilota(id).subscribe(() => this.caricaPiloti());
    }
  }
}