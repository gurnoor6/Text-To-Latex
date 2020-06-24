import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  Myfile : File = null;
  Mytext:string;
  visible=true;


  constructor(private http:HttpClient) { }

  ngOnInit(): void {
  }

  public imagePath;
  imgURL: any;
  public message: string;


  onFileListener(event){
    this.Myfile = event.target.files[0];
  }
 
  preview(files) {
    
    if (files.length === 0)
      return;
    
    var mimeType = files[0].type;
    if (mimeType.match(/image\/*/) == null) {
      this.message = "Only images are supported.";
      return;
    }
 
    var reader = new FileReader();
    this.imagePath = files;
    reader.readAsDataURL(files[0]); 
    reader.onload = (_event) => { 
      this.imgURL = reader.result; 
    }
  };

  onUpload(){
    this.visible=false;
    let id = ((Date.now() as any) as string);
    const fd = new FormData();
    fd.append('identifier',id);
    fd.append('picture',this.Myfile,this.Myfile.name);

    this.http.post('http://127.0.0.1:8000/convert/',fd)
      .subscribe(res => {
        console.log(res);
        const rd = new FormData();
        rd.append('identifier',id);
        this.http.post('http://127.0.0.1:8000/gettext/',rd)
        .subscribe(resp => {
          console.log(resp);
          this.Mytext = resp['response'];
        }); 
      });
  };

  onReset(){
    this.visible=true;
    this.Mytext="";
    this.imgURL="";
    this.Myfile= null;

  };

}
