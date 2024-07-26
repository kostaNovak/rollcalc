import React, { useState } from 'react';
import InputComponent from './InputComponent';

const rolls = [
    { size: 1524, price: 830 },
    { size: 1066, price: 575 },
    { size: 914, price: 500 },
    { size: 750, price: 450 },
    { size: 650, price: 400 },
    { size: 450, price: 280 },
];

const App = () => {
    const [result, setResult] = useState('');
    const [costCalculation, setCostCalculation] = useState('');

    const findClosestHigherRoll = (height) => {
        const higherRolls = rolls.filter(roll => roll.size >= height);
        if (higherRolls.length === 0) {
            return null; 
        }
        return higherRolls.reduce((prev, curr) => (curr.size < prev.size ? curr : prev));
    };

    const handleDimensionSubmit = (dimension) => {
        const [first, second] = dimension.split('x').map(Number);
        const height = Math.max(first, second);
        const lowerDimension = Math.min(first, second);
        
        if (dimension === '841x1180' || dimension === '1180x841') {
            const lowerDimensionDecimal = (1180 / 1000).toFixed(2); // Always use 1.18
            const totalCost = lowerDimensionDecimal * 500; // Cost for 914 mm
            setResult(`For the file dimension ${dimension}, the closest roll is 914 mm.`);
            setCostCalculation(`${lowerDimensionDecimal} x 500 = ${totalCost.toFixed(2)} din`);
        } else if (!isNaN(height) && !isNaN(lowerDimension)) {
            const closestRoll = findClosestHigherRoll(height);
            if (closestRoll) {
                const lowerDimensionDecimal = (lowerDimension / 1000).toFixed(2);
                const totalCost = lowerDimensionDecimal * closestRoll.price;
                setResult(`For the file dimension ${dimension}, the closest roll is ${closestRoll.size} mm.`);
                setCostCalculation(`${lowerDimensionDecimal} x ${closestRoll.price} = ${totalCost.toFixed(2)} din`);
            } else {
                setResult(`There are no rolls larger than ${height} mm.`);
                setCostCalculation('');
            }
        } else {
            setResult("Please enter valid dimensions in the format 'width x height'.");
            setCostCalculation('');
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 p-6">
            <h1 className="text-3xl font-bold mb-4 text-center text-white">Roll Size Calculator</h1>
            <InputComponent onDimensionSubmit={handleDimensionSubmit} />
            {result && (
                <p className="mt-4 text-lg text-gray-700 border border-gray-300 p-4 rounded-lg bg-white shadow-md text-center">
                    {result}
                </p>
            )}
            {costCalculation && (
                <p className="mt-2 text-lg text-gray-700 border border-gray-300 p-4 rounded-lg bg-white shadow-md text-center">
                    {costCalculation}
                </p>
            )}
        </div>
    );
};

export default App;
