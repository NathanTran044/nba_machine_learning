import './App.css';
import React, { useState, useEffect } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';


function App() {
  const [data, setData] = useState();
  const [submitFlag, setSubmitFlag] = useState(false)
  const [yearChosenFlag, setYearChosenFlag] = useState(false)
  const [namesList, setNamesList] = useState([])

  useEffect(() => {
    if (submitFlag) {
      console.log("submit useEffect ran")
      fetch(`http://localhost:5100/salary?desired_player=${inputValue.desired_player}&desired_player_year=${inputValue.desired_player_year}&desired_year=${inputValue.desired_year}`)
        .then((response) => response.text())
        .then((responseData) => {
          setData(responseData);
          setSubmitFlag(false);
          console.log(responseData);
        })
        .catch((error) => {
          console.error(error);
        });
    } else if (yearChosenFlag) {
      console.log("year useEffect ran")
      fetch(`http://localhost:5100/names?desired_player_year=${inputValue.desired_player_year}`)
        .then((response) => response.json())
        .then((responseData) => {
          setNamesList(responseData);
          setYearChosenFlag(false);
          console.log(responseData);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [submitFlag, yearChosenFlag]);

  const [inputValue, setInputValue] = useState({
    desired_player: '',
    desired_player_year: '',
    desired_year: ''
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setInputValue((prevState) => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleYearChange = (event) => {
    setYearChosenFlag(true);
    const { name, value } = event.target;
    setInputValue((prevState) => ({
      ...prevState,
      [name]: value
    }));
  }

  function getParams() {
    setSubmitFlag(true);
  }

  function resetParams() {
    setInputValue({
      desired_player: '',
      desired_player_year: '',
      desired_year: ''
    })
  }

  const years = [
    1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
    2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
    2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
  ];
  
  return (
    <div>
      <Select
          name='desired_player_year'
          value={inputValue.desired_player_year}
          label="Year"
          onChange={handleYearChange}
        >
          {years.map((year) => (
            <MenuItem key={year} value={year}>
              {year}
            </MenuItem>
          ))}
      </Select>
      <Autocomplete
        options={namesList} 
        value={inputValue.desired_player}
        onChange={(event, newValue) => handleInputChange({ target: { name: 'desired_player', value: newValue } })}
        renderInput={(params) => (
        <TextField
          {...params}
          name="desired_player"
          label="Player"
          onChange={handleInputChange}
        ></TextField>
      )}
      ></Autocomplete>
      <input type="text" name="desired_year" value={inputValue.desired_year} onChange={handleInputChange}>

      </input>
      <button
        onClick={getParams}
      >submit
      </button>
      <button
        onClick={resetParams}
      >reset
      </button>
      {data}
    </div>
  );
}

export default App;
