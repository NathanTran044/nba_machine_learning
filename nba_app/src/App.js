import './App.css';
import React, { useState, useEffect, toFixed } from 'react';
import {Autocomplete, TextField, Select, MenuItem, Button, InputLabel, FormControl} from '@mui/material';


function App() {
  const [data, setData] = useState();
  const [submitFlag, setSubmitFlag] = useState(false)
  const [yearChosenFlag, setYearChosenFlag] = useState(false)
  const [playerChosenFlag, setPlayerChosenFlag] = useState(false)
  const [namesList, setNamesList] = useState([])
  const [stats, setStats] = useState([])
  const [display, setDisplay] = useState(false);
  const [newName, setNewName] = useState('');
  const [inputValue, setInputValue] = useState({
    desired_player: '',
    desired_player_year: '',
    desired_year: ''
  });
  const playerStatsOrder = [
    'Age', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
    '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB',
    'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'
  ];

  useEffect(() => {
    if (submitFlag) {
      console.log("submit useEffect ran")
      fetch(`http://localhost:5100/salary?desired_player=${inputValue.desired_player}&desired_player_year=${inputValue.desired_player_year}&desired_year=${inputValue.desired_year}`)
        .then((response) => response.text())
        .then((responseData) => {
          setData(responseData);
          setNewName(inputValue.desired_player);
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
    } else if (playerChosenFlag) {
      console.log("player useEffect ran")
      fetch(`http://localhost:5100/stats?desired_player=${inputValue.desired_player}&desired_player_year=${inputValue.desired_player_year}`)
        .then((response) => response.json())
        .then((responseData) => {
          const sortedStats = Object.fromEntries(
            playerStatsOrder.map((key) => [key, responseData[key]])
          );
          setStats(sortedStats);
          setPlayerChosenFlag(false);
          console.log(sortedStats);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [submitFlag, yearChosenFlag, playerChosenFlag]);

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
      [name]: value,
      desired_player: ''
    }));
  }

  function getParams() {
    setStats(null);
    const { desired_player, desired_player_year, desired_year } = inputValue;
    if (desired_player && desired_player_year && desired_year) {
      setPlayerChosenFlag(true);
      setSubmitFlag(true);
      setDisplay(true);
    }
  }

  function resetParams() {
    setInputValue({
      desired_player: '',
      desired_player_year: '',
      desired_year: ''
    })
    setNamesList([]);
    setDisplay(false);
  }

  const years = [
    1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
    2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
    2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
  ];
  
  return (
    <div className='parent'>
      <div class="header">
        <h1>Salaray Predictor</h1>
        <p>See how much an NBA player would make in a different year!</p>
      </div>
      <div className='host'>
        <div>
          <p className='text-1'>Choose the Year of the Player You Want to View</p>
          <FormControl>
            <InputLabel className='year_label-1' id="year-label-1">Year</InputLabel>
            <Select
                className='desired_player_year'
                name='desired_player_year'
                value={inputValue.desired_player_year}
                labelId='year-label-1'
                label='Year'
                onChange={handleYearChange}
              >
                {years.map((year) => (
                  <MenuItem key={year} value={year}>
                    {year}
                  </MenuItem>
                ))}
            </Select>
          </FormControl>
          <p className='text-2'>Choose the Player You Want to View</p>
          <Autocomplete
            className='desired_player'
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
          <p className='text-3'>Choose a Year to Place This Player In</p>
          <FormControl>
            <InputLabel className='year_label-2' id="year-label-2">Year</InputLabel>
            <Select
                className='desired_year'
                name='desired_year'
                value={inputValue.desired_year}
                labelId='year-label-2'
                label='Year'
                onChange={handleInputChange}
              >
                {years.map((year) => (
                  <MenuItem key={year} value={year}>
                    {year}
                  </MenuItem>
                ))}
            </Select>
          </FormControl>
        </div>
        <div>
          <button
            className='submit_button'
            onClick={getParams}
          >
            Submit
          </button>
          <button
            className='reset'
            onClick={resetParams}
          >
            Reset
          </button>
        </div>
      </div>
      <div className='client'>
        {display && stats && data && newName &&(
        <>
          <p className='name'>{newName}</p>
          <div className='stats-wrapper'>
            <div className='stats-column'>
              {playerStatsOrder.slice(0, Math.ceil(playerStatsOrder.length / 2)).map((key) => (
                <p key={key}>{key}: {stats[key]}</p>
              ))}
            </div>
            <div className='stats-column'>
              {playerStatsOrder.slice(Math.ceil(playerStatsOrder.length / 2)).map((key) => (
                <p key={key}>{key}: {stats[key]}</p>
              ))}
            </div>
          </div>
        </>
        )}
      </div>
      <div>
      {display && (
        <>
        {data && stats && (
          <p className='salary'>
            Salary: ${Number(data).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
          </p>
        )}
        </>
      )}
      </div>
    </div>
  );
}

export default App;
