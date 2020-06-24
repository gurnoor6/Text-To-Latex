import { OnInit,Component } from '@angular/core';
import {ApiService} from '../services/api.service';
import { LoadingController } from '@ionic/angular';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  text;
  image;
  constructor(private postservice:ApiService, 
  			  private loadingController:LoadingController,
  			  private _sanitizer: DomSanitizer) {}
  ngOnInit(){
  	console.log(Date.now());
  }

  fileToUpload :File=null;
	handleFileInput(files:FileList,autoUpdate=0){
		this.fileToUpload = files.item(0);
		var reader = new FileReader();
	    reader.readAsDataURL(this.fileToUpload);
	    reader.onload = (event)=>{
	    	this.image = event.target.result;
	    }
	}

   addImage(){
   	(document.querySelector("#image") as any).click();
   }

   async submit(){

	   	const loading = await this.loadingController.create({
	   	  cssClass:'spinner',
	      spinner:'crescent',
	      message: 'Loading...',
	      translucent: true,
	      backdropDismiss: true
	    });

	    await loading.present();

		let id = ((Date.now() as any) as string);
		const formData = new FormData();
		formData.append('identifier',id);
		formData.append('picture',this.fileToUpload,this.fileToUpload.name);
		this.postservice.create('http://localhost:8000'+'/convert/',formData)
			.subscribe(response=>{
				console.log(response);
				this.image = response['picture'];
				const fd = new FormData();
				fd.append('identifier',id);
				this.postservice.create('http://localhost:8000'+'/gettext/',fd)
					.subscribe(response=>{
						console.log(response)
						this.text = response['response'];
						loading.dismiss();
					});
			});

	}

	reset(){
		this.image="";
		this.text="";
	}
}
