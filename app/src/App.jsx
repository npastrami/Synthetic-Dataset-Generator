import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { FilePicker } from './file-picker';
import logo from './assets/images/logo.png';

function App() {
  const [files, setFiles] = useState(null);
  const convertFiles = () => {
    axios.post('/convert')
      .then(response => {
        console.log(response.data);  // Log server response
      })
      .catch(error => {
        console.error(error);  // Log any errors
      });
  };

  const downloadStream = () => {  
    axios.get('/download', {responseType: 'blob'})
      .then(resp => {
          const url = window.URL.createObjectURL(new Blob([resp.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'all_files.zip'); 
          document.body.appendChild(link);
          link.click();
      })
      .catch(() => alert('Download failed!'));
  };

  const processOcrScan = () => {
    axios.post('/craft')
      .then(response => {
        console.log(response.data);  // Log server response
      })
      .catch(error => {
        console.error(error);  // Log any errors
      });
  };

  // how can we make makeMISCopies and makeINTCopies more DRY? What is Dry?
  // DRY = Don't Repeat Yourself
  const makeCopies = (form_type) => {
    axios.post('/makecopies', { form_type })
      console.log(form_type)
      .then(response => {
        console.log(`POST request to /makeCopies for ${form_type} was successful`, response.data);
      })
      .catch(error => {
        console.error(`POST request to /makeCopies for ${form_type} failed`, error);
      });
  };

  return (
    <div className="App">
      <h1>Generator</h1>
      <div className="card">
        <FilePicker accept=".pdf,.xlsx" uploadURL="/upload" />
      </div>
      <div className="sidebar">
       {/* how can we make each button trigger the make_copies function and route and each button pass the form_type associated with that butt */}
        <button onClick={processOcrScan} >OCR Scan</button>
        <button onClick={downloadStream}>Download All</button>
        <button onClick={() => makeCopies('MIS')}>Make MIS Copies</button>
        <button onClick={() => makeCopies('INT')}>Make INT Copies</button>
        <button onClick={() => makeCopies('DIV')}>Make DIV Copies</button>
        <button onClick={() => makeCopies('MISC')}>Make MISC Copies</button>
        <button onClick={() => makeCopies('CON1099')}>Make con1099 Copies</button>
        <button onClick={() => makeCopies('CONV2')}>Make con1099-v2 Copies</button>
        <button onClick={() => makeCopies('SA')}>Make 1099-SA Copies</button>
        <button onClick={() => makeCopies('NEC')}>Make 1099-NEC Copies</button>
        <button onClick={() => makeCopies('K1065K1')}>Make 1065 K1 Copies</button>
        <button onClick={() => makeCopies('1120SK1')}>Make 1120s K1 Copies</button>
        <button onClick={() => makeCopies('Q')}>Make 1099-q Copies</button>
      </div>
      <p className="read-the-docs">
        ---
      </p>
    </div>
  );
}

export default App;