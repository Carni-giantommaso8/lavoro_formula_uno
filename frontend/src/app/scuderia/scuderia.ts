import { Component, OnInit, signal } from '@angular/core';
import { ScuderiaService } from './scuderia.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-scuderia',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './scuderia.html',
  styleUrl: './scuderia.css'
})
export class ScuderiaComponent implements OnInit {
  scuderie = signal<any[]>([]);
  sponsor = signal<any[]>([]);
  mostraForm = signal(false);
  scuderiaInModifica = signal<number |null>(null);
  nuovaScuderia = {
    nome: '',
    team_principal: '',
    costruttore_motore: '',
    anno_fondazione: null,
    id_sponsor: null
  };

  constructor(private service: ScuderiaService) {}

  ngOnInit() {
    this.caricaDati();
    this.caricaSponsor();
  }

  caricaDati() {
    this.service.getScuderie().subscribe((dati: any) => {
      console.log("DATI RICEVUTI DA FLASK:", dati);
      
      this.scuderie.set(dati); 
    });
  }

  caricaSponsor(){
    this.service.getSponsor().subscribe((dati:any)=>{
      this.sponsor.set(dati);
    });
  }

  avviaModifica(scuderia: any){
    this.scuderiaInModifica.set(scuderia.id);
    this.nuovaScuderia={
      nome:scuderia.nome,
      team_principal: scuderia.team_principal,
      costruttore_motore: scuderia.costruttore_motore,
      anno_fondazione: scuderia.anno_fondazione,
      id_sponsor: scuderia.id_sponsor
    };
    this.mostraForm.set(true);
  }

  annullaForm(){
    this.mostraForm.set(false);
    this.scuderiaInModifica.set(null);
    this.nuovaScuderia={nome: '', team_principal: '', costruttore_motore: '', anno_fondazione: null, id_sponsor: null};
  }

  salvaScuderia(){
    const id = this.scuderiaInModifica();

    if(id){ //vogliamo modificare
      this.service.updateScuderia(id, this.nuovaScuderia).subscribe(() =>{
        this.caricaDati();
        this.annullaForm();
      });
    }else{ //inserimento
      this.service.addScuderia(this.nuovaScuderia).subscribe(()=>{
        this.caricaDati();
        this.annullaForm();
      });
    }
  }

  elimina(id: number) {
    if(confirm("Sei sicuro di voler eliminare questa scuderia? L'azione è irreversibile!")) {
      this.service.deleteScuderia(id).subscribe(() => {
        this.caricaDati();
      });
    }
  }

}