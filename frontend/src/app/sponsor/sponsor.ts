import { Component, OnInit, signal } from '@angular/core';
import { SponsorService } from './sponsor.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-sponsor',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './sponsor.html',
  styleUrl: './sponsor.css'
})
export class SponsorComponent implements OnInit{
    sponsors=signal<any[]>([]);
    mostraForm = signal(false);
    sponsorInModifica = signal<number | null>(null);

    nuovoSponsor = {
        nome_societa: '',
        settore_merceologico: '',
        valore_contratto_annuo: null as number | null,
        scadenza_contratto: ''
    };

    constructor(private service: SponsorService) {}

    ngOnInit(){
        this.caricaSponsors();
    }

    caricaSponsors(){
        this.service.getSponsors().subscribe((dati:any)=>{
            this.sponsors.set(dati);
        });
    }

    avviaModifica(sp:any){
        this.sponsorInModifica.set(sp.id);

        const dataFormattata = sp.scadenza_contratto ? sp.scadenza_contratto.split('T')[0]:'';

        this.nuovoSponsor={
            nome_societa: sp.nome_societa,
            settore_merceologico: sp.settore_merceologico,
            valore_contratto_annuo: sp.valore_contratto_annuo,
            scadenza_contratto: dataFormattata
        };
        this.mostraForm.set(true);
    }

    annullaForm(){
        this.mostraForm.set(false);
        this.sponsorInModifica.set(null);
        this.nuovoSponsor = { nome_societa: '', settore_merceologico: '', valore_contratto_annuo: null, scadenza_contratto: '' };
    }

    salvaSponsor() {
        const id = this.sponsorInModifica();
        if (id) {
        this.service.updateSponsor(id, this.nuovoSponsor).subscribe(() => {
            this.caricaSponsors();
            this.annullaForm();
        });
        } else {
        this.service.addSponsor(this.nuovoSponsor).subscribe(() => {
            this.caricaSponsors();
            this.annullaForm();
        });
        }
    }

    elimina(id: number) {
        if (confirm("Sei sicuro di voler eliminare questo sponsor? Le scuderie collegate perderanno lo sponsor (diventerà NULL).")) {
        this.service.deleteSponsor(id).subscribe(() => {
            this.caricaSponsors();
        });
        }
    }
}