import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  

  constructor(private httpClient:HttpClient) {}

  private url = "";

  create(url,post){
     return this.httpClient.post<any>(url,post);
  }
}