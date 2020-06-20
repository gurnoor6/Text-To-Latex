import { OnInit,Component } from '@angular/core';
import {ApiService} from '../services/api.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  text;
  constructor(private postservice:ApiService) {}
  ngOnInit(){
  	console.log(Date.now());
  }

  fileToUpload :File=null;
	handleFileInput(files:FileList,autoUpdate=0){
		this.fileToUpload = files.item(0);
		this.test();
   }

   test(){
		let id = ((Date.now() as any) as string);
		const formData = new FormData();
		formData.append('identifier',id);
		formData.append('picture',this.fileToUpload,this.fileToUpload.name);
		this.postservice.create('http://importfreshie.pythonanywhere.com'+'/convert/',formData)
			.subscribe(response=>{
				console.log(response);
				const fd = new FormData();
				fd.append('identifier',id);
				this.postservice.create('http://importfreshie.pythonanywhere.com'+'/gettext/',fd)
					.subscribe(response=>{
						console.log(response)
						this.text = response['response'];
					});
			});

	}
}
