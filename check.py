{
  "meta": {
    "version": 319,
    "companyId": "EC661390fcydRgwMNKuDaRNYpP2fFa52",
    "userId": "Hp8PIKQ7famTb661395c8t0I4i9PY2ed",
    "name": "אמת",
    "imageRef": "",
    "date": "2025-02-19T09:35:15.564Z"
  },
  "schemaGroups": [
    {
      "dictionarySchemas": [
        {
          "pullRequest": {
            "dataEncoding": "win1255",
            "skipEncoding": false,
            "host": "sftp.jafora-tabori.co.il",
            "port": 22,
            "username": "getruck",
            "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC/XJva03yFnbQQXyME2zTvwO8cAH8Nk6AYW7pBJNiAXgCj3+1X\ngUAC7Uof/ZKh0PgTBFBVbWqVi/3fsC1Hb9hNmnwj4wcGzk1EUIplj0Fjq2wmZ1e9\nUm9DSn9v3Z1OLZPEFQRr3NKY+L/YT6OTpmMAswLlBiddjjPMGbw9U/rEhwIDAQAB\nAoGAPewixtm+pqIUfWO7ujuQ0rBU73O9qVAG8zrjd2cL4+YHQQAaFkHNy+SrItT0\nGQa877JqqGoinkfRnAuvazlm/Y5WYR300PbNh0pmRicfaxkV85ouBkbqL0UM7vwc\nbTn5+uwIbOttEwb3vLBxyukz4nysLzIIyM2SEe77uvRYeAECQQDlJcQbrvoRvZlU\nrL07UKD2A7SeAw+0c37UrJMlW53+GFPoyz0erLstqqFrh+EP9D593+y7Vc8xWz9K\na564S/CHAkEA1clNH8rjApHjT24P4ma4cRhIENjFXMq3/+guFL5MUC5sXr0ED035\ndevfrCB8VqMnEfbZpvXhlEeaA/BHHPOMAQJBALuvvjvqitrjD+biAbDGrsAycssF\nuORVwSmTHIb5zqOj635+kVZBpqKV4tc/mWFG7bSOJ8mdVDKaCXH8Simr0ZsCQCIZ\nMnDwtlaRmFTx9ByjT6XSPqRZPtl3B/QMP1VVqOxdCzHtKfma8UAKuClHIS3cZf3q\nhnqn2ywAY6NfLqiCfAECQGZHQyLOrMSN69anVZn1OPrD/HrJR0w7vokItrGrYz0Y\n5HBL6Jjrl8Q7mPXleNePsaYQMKwn42qJotC5pTz+yTI=\n-----END RSA PRIVATE KEY-----",
            "toDelete": false,
            "remotePath": {
              "func": "(args) => { return `/From_Afek/Region_${args.category}/GTLAKD_${args.category}.TXT`;}"
            }
          },
          "transformers": [],
          "dataFormat": "txt",
          "identifierName": "placeholder-dont-delete",
          "extraProcessing": {
            "func": "(rawData, dictionary, extraData) => {\n  // Constants for field positions\n  const FIELDS = {\n    CUSTOMER_ID: { start: 0, end: 15 },\n    CUSTOMER_NAME: { start: 15, end: 46 },\n    STREET: { start: 46, end: 75 },\n    CITY: { start: 75, end: 105 },\n    CUSTOMER_CHARACTERIZATION: { start: 113, end: 117 },\n    TIME_WINDOWS_BLOCK: { start: 118, end: 148 },\n    DELIVERY_DAYS: { start: 149, end: 155 },\n    DISTRIBUTION_SNIF: { start: 154, end: 174 },\n    BUSINESS_CHARACTERIZATION: { start: 195, end: 214 },\n    SALES_BRANCH: { start: 214, end: 217 },\n  };\n\n  const extractField = (row, field) => row.slice(field.start, field.end).trim();\n\n  const parseTimeWindows = (row) => {\n    const timeBlock = extractField(row, FIELDS.TIME_WINDOWS_BLOCK);\n    const windows = [];\n\n    // Match groups of 4 digits followed by 4 digits\n    const timeMatches = timeBlock.match(/(\\d{2}:\\d{2})(\\d{2}:\\d{2})/g) || [];\n\n    for (const match of timeMatches) {\n      const timeStr = match.toString();\n\n      // Extract hours and minutes for both times\n      const time1Hours = parseInt(timeStr.slice(0, 2));\n      const time1Minutes = parseInt(timeStr.slice(3, 5));\n      const time2Hours = parseInt(timeStr.slice(5, 7));\n      const time2Minutes = parseInt(timeStr.slice(8, 10));\n\n      // Convert to comparable numbers (minutes since midnight)\n      const time1Total = time1Hours * 60 + time1Minutes;\n      const time2Total = time2Hours * 60 + time2Minutes;\n\n      // Format times with leading zeros\n      const formatTime = (hours, minutes) =>\n        `${hours.toString().padStart(2, \"0\")}:${minutes.toString().padStart(2, \"0\")}`;\n\n      // Create time window with earlier time first\n      const timeWindow =\n        time1Total <= time2Total\n          ? `${formatTime(time1Hours, time1Minutes)}-${formatTime(time2Hours, time2Minutes)}`\n          : `${formatTime(time2Hours, time2Minutes)}-${formatTime(time1Hours, time1Minutes)}`;\n\n      if (!windows.includes(timeWindow)) {\n        windows.push(timeWindow);\n      }\n    }\n\n    return windows;\n  };\n\n  const createCustomerEntry = (row) => ({\n    customerDays: extractField(row, FIELDS.DELIVERY_DAYS).split(\"\"),\n    distributionSnif: extractField(row, FIELDS.DISTRIBUTION_SNIF),\n    salesBranch: extractField(row, FIELDS.SALES_BRANCH),\n    customerName: extractField(row, FIELDS.CUSTOMER_NAME) || \"שם לקוח לא תקין\",\n    itemUnloadAddress: `${extractField(row, FIELDS.STREET)}, ${extractField(row, FIELDS.CITY)}`,\n    customerCharacterization: extractField(row, FIELDS.CUSTOMER_CHARACTERIZATION),\n    businessCharacterization: extractField(row, FIELDS.BUSINESS_CHARACTERIZATION),\n    deliveryTimeWindows: {},\n  });\n\n  // Main processing\n  const customersData = {};\n  const days = [\"א\", \"ב\", \"ג\", \"ד\", \"ה\", \"ו\"];\n\n  try {\n    for (const row of rawData) {\n      // Skip empty rows\n      if (!row.trim()) continue;\n\n      const customerId = extractField(row, FIELDS.CUSTOMER_ID);\n      if (!customerId) continue;\n\n      // Create or get existing customer data\n      if (!customersData[customerId]) {\n        customersData[customerId] = createCustomerEntry(row);\n      }\n\n      // Process delivery days and time windows\n      const customerDays = extractField(row, FIELDS.DELIVERY_DAYS).split(\"\").filter(Boolean);\n      const timeWindows = parseTimeWindows(row);\n\n      // Update customer days (unique values, sorted)\n      customersData[customerId].customerDays = Array.from(\n        new Set([...customersData[customerId].customerDays, ...customerDays])\n      ).sort();\n\n      // Update time windows for each day\n      customerDays.forEach((day) => {\n        const dayIndex = days.indexOf(day);\n        if (dayIndex !== -1 && timeWindows.length > 0) {\n          // Initialize array if doesn't exist\n          if (!customersData[customerId].deliveryTimeWindows[dayIndex]) {\n            customersData[customerId].deliveryTimeWindows[dayIndex] = [];\n          }\n\n          // Add new time windows avoiding duplicates\n          timeWindows.forEach((window) => {\n            if (!customersData[customerId].deliveryTimeWindows[dayIndex].includes(window)) {\n              customersData[customerId].deliveryTimeWindows[dayIndex].push(window);\n            }\n          });\n        }\n      });\n    }\n\n    return { customersData };\n  } catch (error) {\n    console.error(\"Error processing delivery data:\", error);\n    return { customersData: {}, error: error.message };\n  }\n}"
          }
        },
        {
          "pullRequest": {
            "body": {
              "func": "(...args) => (`{\"entityName\":\"customer\",\"query\":{\"select\":{\"externalId\":true,\"id\":true,\"name\":true,\"addressLat\":true,\"addressLng\":true,\"serviceTimeId\":true,\"isBase\":true,\"isNetwork\":true},\"where\":{\"externalId\":{\"not\":null}}},\"companyId\":\"EC661390fcydRgwMNKuDaRNYpP2fFa52\"}`)"
            },
            "dataEncoding": "utf8",
            "skipEncoding": false,
            "endpoint": {
              "func": "({workingDates}) => `https://jafora.getruck.co.il/api/erp2/api-data/read`"
            },
            "method": "POST",
            "headers": {
              "Content-Type": "application/json",
              "Authorization": "Bearer jaforaIbQV5zBKgzrNtcoh1KibHm1FNO7ZW7oz0uDqdGYMZLSAtgfMCDKszWuuRv",
              "Connection": "keep-alive",
              "Accept": "*/*",
              "Accept-Encoding": "gzip, deflate, br"
            }
          },
          "transformers": [
            {
              "from": "externalId",
              "to": "id"
            },
            {
              "from": "addressLat",
              "to": "itemUnloadLatitude",
              "func": {
                "func": "(x) => String(x)"
              }
            },
            {
              "from": "addressLng",
              "to": "itemUnloadLongitude",
              "func": {
                "func": "(x) => String(x)"
              }
            },
            {
              "from": "serviceTimeId",
              "to": "customFields.13"
            },
            {
              "from": [
                "addressLng",
                "addressLat"
              ],
              "to": "customFields.11",
              "func": {
                "func": "(lon, lat) => `${lon},${lat}`"
              }
            },
            {
              "from": "isBase",
              "to": "isBase"
            },
            {
              "from": "isNetwork",
              "to": "isNetwork"
            }
          ],
          "dataFormat": "json",
          "dataPath": "data",
          "identifierName": "customerId"
        }
      ],
      "schemas": [
        {
          "pullRequest": {
            "dataEncoding": "win1255",
            "skipEncoding": false,
            "host": "sftp.jafora-tabori.co.il",
            "port": 22,
            "username": "getruck",
            "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC/XJva03yFnbQQXyME2zTvwO8cAH8Nk6AYW7pBJNiAXgCj3+1X\ngUAC7Uof/ZKh0PgTBFBVbWqVi/3fsC1Hb9hNmnwj4wcGzk1EUIplj0Fjq2wmZ1e9\nUm9DSn9v3Z1OLZPEFQRr3NKY+L/YT6OTpmMAswLlBiddjjPMGbw9U/rEhwIDAQAB\nAoGAPewixtm+pqIUfWO7ujuQ0rBU73O9qVAG8zrjd2cL4+YHQQAaFkHNy+SrItT0\nGQa877JqqGoinkfRnAuvazlm/Y5WYR300PbNh0pmRicfaxkV85ouBkbqL0UM7vwc\nbTn5+uwIbOttEwb3vLBxyukz4nysLzIIyM2SEe77uvRYeAECQQDlJcQbrvoRvZlU\nrL07UKD2A7SeAw+0c37UrJMlW53+GFPoyz0erLstqqFrh+EP9D593+y7Vc8xWz9K\na564S/CHAkEA1clNH8rjApHjT24P4ma4cRhIENjFXMq3/+guFL5MUC5sXr0ED035\ndevfrCB8VqMnEfbZpvXhlEeaA/BHHPOMAQJBALuvvjvqitrjD+biAbDGrsAycssF\nuORVwSmTHIb5zqOj635+kVZBpqKV4tc/mWFG7bSOJ8mdVDKaCXH8Simr0ZsCQCIZ\nMnDwtlaRmFTx9ByjT6XSPqRZPtl3B/QMP1VVqOxdCzHtKfma8UAKuClHIS3cZf3q\nhnqn2ywAY6NfLqiCfAECQGZHQyLOrMSN69anVZn1OPrD/HrJR0w7vokItrGrYz0Y\n5HBL6Jjrl8Q7mPXleNePsaYQMKwn42qJotC5pTz+yTI=\n-----END RSA PRIVATE KEY-----",
            "toDelete": false,
            "remotePath": {
              "func": "(args) => { return `/From_Afek/Region_${args.category}/GTAZM_${args.category}.TXT`;}"
            },
            "backupPath": {
              "func": "(...args) => { const thisTime = new Date(); const timestamp = `${thisTime.getFullYear()}${String(thisTime.getMonth() + 1).padStart(2, '0')}${String(thisTime.getDate()).padStart(2, '0')}_${String(thisTime.getHours()).padStart(2, '0')}${String(thisTime.getMinutes()).padStart(2, '0')}${String(thisTime.getSeconds()).padStart(2, '0')}`;  return `/From_Afek/Region_${args[0].category}/BackupGT/GTAZM_${args[0].category}_${timestamp}.TXT`}"
            }
          },
          "transformers": [
            {
              "from": "row",
              "to": "customerId",
              "func": {
                "func": "(row) => row.slice(0, 15).trim()"
              }
            },
            {
              "from": [
                "customerId",
                "extraData.dictionaries.customersData"
              ],
              "to": "customerName",
              "func": {
                "func": "(id, data) => data[id]?.customerName"
              }
            },
            {
              "from": [
                "customerId",
                "extraData.dictionaries.customersData"
              ],
              "to": "itemUnloadAddress",
              "func": {
                "func": "(id, data) => data[id]?.itemUnloadAddress"
              }
            },
            {
              "from": [
                "customerId",
                "extraData.dictionaries.customersData",
                "extraData.workingDates"
              ],
              "to": "customFields.2",
              "func": {
                "func": "(customerId, customersData, workingDates) => { const timeWindows = customersData?.[customerId]?.deliveryTimeWindows; return (timeWindows?.['0'] || [])?.join(', ') || ':'; }"
              }
            },
            {
              "from": [
                "customerId",
                "extraData.dictionaries.customersData",
                "extraData.workingDates"
              ],
              "to": "calculatedTimeWindow",
              "func": {
                "func": "(customerId, customersData, workingDates) => {\n  const timeWindows = customersData[customerId]?.deliveryTimeWindows[0];\n\n  if (!timeWindows || Object.keys(timeWindows).length === 0) {\n    return \"06:00-14:00\"; // Default fallback if no entries exist\n  }\n\n  // Get all time windows\n  const allTimeWindows = Object.values(timeWindows);\n\n  // Extract hours from all time windows\n  const hours = allTimeWindows.reduce((acc, timeWindow) => {\n    const [start, end] = timeWindow.split(\"-\");\n    const startHour = parseInt(start.split(\":\")[0]);\n    const startMinute = parseInt(start.split(\":\")[1]);\n    const endHour = parseInt(end.split(\":\")[0]);\n    const endMinute = parseInt(end.split(\":\")[1]);\n\n    acc.push({\n      hour: startHour,\n      minute: startMinute,\n      isStart: true,\n    });\n    acc.push({\n      hour: endHour,\n      minute: endMinute,\n      isStart: false,\n    });\n    return acc;\n  }, []);\n\n  // Find min start time and max end time\n  const startTimes = hours.filter((t) => t.isStart);\n  const endTimes = hours.filter((t) => !t.isStart);\n\n  const minStart = startTimes.reduce((min, curr) => {\n    if (curr.hour < min.hour || (curr.hour === min.hour && curr.minute < min.minute)) {\n      return curr;\n    }\n    return min;\n  }, startTimes[0]);\n\n  const maxEnd = endTimes.reduce((max, curr) => {\n    if (curr.hour > max.hour || (curr.hour === max.hour && curr.minute > max.minute)) {\n      return curr;\n    }\n    return max;\n  }, endTimes[0]);\n\n  // Format the result\n  const formatTime = (hour, minute) => `${hour.toString().padStart(2, \"0\")}:${minute.toString().padStart(2, \"0\")}`;\n\n  return `${formatTime(minStart.hour, minStart.minute)}-${formatTime(maxEnd.hour, maxEnd.minute)}`;\n}"
              }
            },
            {
              "from": "calculatedTimeWindow",
              "to": "deliveryTimeWindows",
              "func": {
                "func": "(timeWindows) => {const x = timeWindows.split(',')[0]; return [([(parseInt(x.split('-')[0].split(':')[0])-2 + '').padStart(2,'0') + ':' + x.split('-')[0].split(':')[1], (parseInt(x.split('-')[1].split(':')[0])-2 + '').padStart(2,'0') + ':' + x.split('-')[1].split(':')[1]]).join('-')]}"
              }
            },
            {
              "from": [
                "customerId",
                "extraData.dictionaries.customersData"
              ],
              "to": "customFields.12",
              "func": {
                "func": "(customerId, customersData) => {return customersData[customerId]?.customerDays}"
              }
            },
            {
              "to": "scheduled",
              "default": 1
            },
            {
              "from": "deliveryTimeWindows",
              "to": "label",
              "func": {
                "func": "(deliveryTimeWindows) => {const lastHour = parseInt(deliveryTimeWindows[0].split('-')[1].split(':')[0]); return (lastHour <= 10) ? '#F03344' : ((lastHour < 14) ? '#11BB22': '#F59E0B');}"
              }
            },
            {
              "to": "comment",
              "default": "-"
            },
            {
              "from": "customerId",
              "to": "customFields.3"
            },
            {
              "from": "customerId",
              "to": "itemDescription",
              "func": {
                "func": "c=>`  מזהה לקוח: ${c}     `"
              }
            },
            {
              "from": "row",
              "to": "customFields.6",
              "func": {
                "func": "(row) => row.slice(15,16)"
              }
            },
            {
              "from": "row",
              "to": "orderId",
              "func": {
                "func": "(row) => row.slice(18, 26).trim()"
              }
            },
            {
              "from": "row",
              "to": "visitType",
              "func": {
                "func": "(row) => {const type = row.slice(26, 27);\n return type == 'O'? 'w2c': 'c2w';}"
              }
            },
            {
              "from": "row",
              "to": "deliveryDate",
              "func": {
                "func": "(row) => {const fullDate = row.slice(27, 37).trim();\nconst d=fullDate.slice(0,2);\nconst m =fullDate.slice(2,4);\nconst y=fullDate.slice(4, 8);\nreturn new Date(`${m}.${d}.${y}`);}"
              }
            },
            {
              "from": [
                "deliveryDate",
                "extraData.workingDates"
              ],
              "to": "sekerKulsheku",
              "func": {
                "func": "(deliveryDate, planDates) => { const planDate = new Date(planDates[0]); return ( deliveryDate.getDate() === planDate.getDate() &&  deliveryDate.getMonth() === planDate.getMonth() &&  deliveryDate.getFullYear() === planDate.getFullYear() ); }"
              },
              "validator": {
                "condition": "x => !x",
                "reason": "מועד האספקה אינו תואם לתאריך התוכנית",
                "severity": "low"
              }
            },
            {
              "to": "amount",
              "default": 1
            },
            {
              "from": "row",
              "to": "weight",
              "func": {
                "func": "(row) => Number(row.slice(53, 69).trim())"
              }
            },
            {
              "from": "row",
              "to": "volume",
              "func": {
                "func": "(row) => Number(row.slice(69, 85).trim())"
              }
            },
            {
              "from": "row",
              "to": "worth",
              "func": {
                "func": "(row) => Number(row.slice(37, 53).trim())"
              }
            },
            {
              "from": "row",
              "to": "customFields.7",
              "func": {
                "func": "(row) => Number(row.slice(85, 101).trim())"
              }
            },
            {
              "from": "row",
              "func": {
                "func": "(row) => row.slice(101, 102).trim() === '8'"
              },
              "validator": {
                "condition": "x => !x",
                "reason": "הזמנה מבוטלת",
                "severity": "low"
              }
            },
            {
              "from": "row",
              "to": "customFields.5",
              "func": {
                "func": "(row) => row.slice(121, 141).trim()"
              }
            },
            {
              "from": "row",
              "to": "customFields.8",
              "func": {
                "func": "(row) => row.slice(156, 157).trim()"
              }
            },
            {
              "from": "row",
              "to": "customFields.9",
              "func": {
                "func": "(row) => row.slice(157, 158).trim()"
              }
            },
            {
              "from": "row",
              "to": "customFields.10",
              "func": {
                "func": "(row) => row.slice(158, 159).trim()"
              }
            },
            {
              "from": [
                "customerId",
                "extraData.dictionaries.customersData"
              ],
              "to": "snif",
              "func": {
                "func": "(customerId, customersData) => {return customersData[customerId]?.distributionSnif}"
              }
            },
            {
              "from": "row",
              "to": "customFields.15",
              "func": {
                "func": "(row) => row.slice(142, 156).trim()"
              }
            },
            {
              "from": "snif",
              "to": "customFields.1"
            },
            {
              "from": "snif",
              "to": "itemLoadAddress",
              "func": {
                "map": {
                  "options": {
                    "20": "צרעה",
                    "30": "בארות יצחק",
                    "60": "ציפורית",
                    "70": "באר שבע"
                  },
                  "default": "בארות יצחק"
                }
              }
            },
            {
              "from": "snif",
              "to": "itemLoadLatitude",
              "func": {
                "map": {
                  "options": {
                    "20": "31.76230",
                    "30": "32.04453",
                    "60": "32.76037",
                    "70": "31.225035"
                  },
                  "default": ""
                }
              },
              "validator": {
                "condition": "x => !x",
                "reason": "מרלוג לא נתמך",
                "severity": "low"
              }
            },
            {
              "from": "snif",
              "to": "itemLoadLongitude",
              "func": {
                "map": {
                  "options": {
                    "20": "34.97867",
                    "30": "34.9082",
                    "60": "35.31783",
                    "70": "34.814937"
                  },
                  "default": ""
                }
              },
              "validator": {
                "condition": "x => !x",
                "reason": "מרלוג לא נתמך",
                "severity": "low"
              }
            },
            {
              "from": [
                "snif",
                "customerId",
                "extraData.dictionaries.customerId"
              ],
              "to": "truckType",
              "func": {
                "func": "(snifNum, customerId, dic) => {let tags = [`DPT${snifNum}`]; if (dic[customerId]?.isBase) tags.push('מאושר_בסיס'); return tags}"
              }
            },
            {
              "from": [
                "customerId",
                "extraData.dictionaries.customerId"
              ],
              "to": "customFields.14",
              "func": {
                "func": "(customerId, dic) => dic[customerId]?.isNetwork ? 'כן':'לא'"
              }
            },
            {
              "from": "customFields.14",
              "to": "priority",
              "func": {
                "func": "(isNetwork) => (isNetwork === 'כן') ? 4 : 1"
              }
            },
            {
              "to": "lineInOrder",
              "default": 1
            },
            {
              "from": [
                "customFields.5",
                "customFields.7",
                "customFields.8",
                "customFields.9",
                "customFields.10"
              ],
              "to": "packageId",
              "func": {
                "func": "(cf5, cf7, cf8, cf9, cf10) => { const obj = { \"customFields.5\":cf5, \"customFields.7\":cf7, \"customFields.8\":cf8, \"customFields.9\":cf9, \"customFields.10\":cf10  }; return JSON.stringify(obj); }"
              }
            }
          ],
          "name": "orders-text",
          "dataFormat": "txt",
          "requiredDictionaries": [
            "customerId"
          ]
        }
      ],
      "extraTransformers": [],
      "mergeConfig": {
        "propertiesMergeMap": {
          "isActive": "override"
        },
        "mergeMode": "ignoreAssociatedLocked"
      },
      "dataType": "orders",
      "name": "ordersPull",
      "isLockEnabled": false
    },
    {
      "dictionarySchemas": [],
      "schemas": [
        {
          "pullRequest": {
            "body": {
              "func": "(...args) => (`{\"entityName\":\"truck\",\"query\":{    \"where\":{\n            \"isActive\": true}},\"companyId\":\"EC661390fcydRgwMNKuDaRNYpP2fFa52\"}`)"
            },
            "dataEncoding": "utf8",
            "skipEncoding": false,
            "endpoint": {
              "func": "({workingDates}) => `https://jafora.getruck.co.il/api/erp2/api-data/read`"
            },
            "method": "POST",
            "headers": {
              "Content-Type": "application/json",
              "Authorization": "Bearer jaforaIbQV5zBKgzrNtcoh1KibHm1FNO7ZW7oz0uDqdGYMZLSAtgfMCDKszWuuRv",
              "Connection": "keep-alive",
              "Accept": "*/*",
              "Accept-Encoding": "gzip, deflate, br"
            }
          },
          "transformers": [
            {
              "from": "id",
              "to": "id",
              "func": {
                "func": "x => String(x)"
              }
            },
            {
              "from": "maxWeight",
              "to": "maxWeight"
            },
            {
              "to": "cost.perKilometer",
              "default": 100
            },
            {
              "to": "cost.perMinute",
              "default": 200
            },
            {
              "to": "cost.dailyFixed",
              "default": 1000
            },
            {
              "from": "maxVolume",
              "to": "maxVolume",
              "default": 1000
            },
            {
              "to": "priority",
              "default": 0
            },
            {
              "from": "plate",
              "to": "plateNumber"
            },
            {
              "to": "routeNumber",
              "default": 0
            },
            {
              "to": "dimensions",
              "func": {
                "func": "(size) => [{length: 7, width: 2.35, height: 1}]"
              }
            },
            {
              "from": "labels",
              "to": "labels",
              "func": {
                "func": "(labels) => labels.split(', ')"
              }
            },
            {
              "from": "type",
              "to": "customFields.0"
            },
            {
              "from": "labels",
              "to": "customFields.1",
              "func": {
                "func": "(labels) => labels.find(e=>e.includes('DPT'))"
              }
            },
            {
              "from": "id",
              "to": "customFields.2",
              "func": {
                "func": "x => String(x)"
              }
            },
            {
              "from": "customFields.1",
              "to": "segment",
              "func": {
                "func": "s => `משאית ${s.substr(3)}`"
              }
            }
          ],
          "name": "trucks-ERP",
          "dataFormat": "json",
          "dataPath": "data",
          "requiredDictionaries": []
        }
      ],
      "mergeConfig": {
        "propertiesMergeMap": {},
        "mergeMode": "ignoreAll"
      },
      "dataType": "trucks",
      "name": "trucks-ERP",
      "isLockEnabled": false
    },
    {
      "dictionarySchemas": [],
      "schemas": [
        {
          "pullRequest": {
            "body": {
              "func": "(...args) => (`{\"entityName\":\"shift\",\"query\":{\"where\":{\"status\":{\"equals\":\"זמין\"}},\"include\":{\"driver\":true}},\"companyId\":\"EC661390fcydRgwMNKuDaRNYpP2fFa52\"}`)"
            },
            "dataEncoding": "utf8",
            "skipEncoding": false,
            "endpoint": {
              "func": "({workingDates}) => `https://jafora.getruck.co.il/api/erp2/api-data/read`"
            },
            "method": "POST",
            "headers": {
              "Content-Type": "application/json",
              "Authorization": "Nissim jaforaIbQV5zBKgzrNtcoh1KibHm1FNO7ZW7oz0uDqdGYMZLSAtgfMCDKszWuuRv",
              "Connection": "keep-alive",
              "Accept": "*/*",
              "Accept-Encoding": "gzip, deflate, br"
            }
          },
          "transformers": [
            {
              "from": "driver.id",
              "to": "id",
              "func": {
                "func": "x => String(x)"
              }
            },
            {
              "from": "driver.phone",
              "to": "phone",
              "func": {
                "func": "x => String(x)"
              }
            },
            {
              "to": "priority",
              "default": 0
            },
            {
              "from": "driver.hasBaseAccess",
              "to": "labels",
              "func": {
                "func": "hasBaseAccess => (hasBaseAccess) ? ['מאושר_בסיס'] : []"
              }
            },
            {
              "from": "driver.name",
              "to": "name"
            },
            {
              "from": "driver.shiftStart",
              "to": "shifts.0.start.time",
              "func": {
                "func": "(t) => !t ? 7 : parseFloat(((t.split(':').map(Number)[0] % 12 + t.split(':').map(Number)[1] / 60 + (t.split(':').map(Number)[0] >= 12 ? 12 : 0)).toFixed(2)))"
              }
            },
            {
              "from": "driver.shiftEnd",
              "to": "shifts.0.end.time",
              "func": {
                "func": "(t) => !t ? 12 : parseFloat(((t.split(':').map(Number)[0] % 12 + t.split(':').map(Number)[1] / 60 + (t.split(':').map(Number)[0] >= 12 ? 12 : 0)).toFixed(2)))"
              }
            },
            {
              "to": "customFields.0",
              "default": "-"
            },
            {
              "from": "depot",
              "to": "customFields.1",
              "func": {
                "map": {
                  "options": {
                    "סניף 20": "20",
                    "סניף 30": "30",
                    "סניף 60": "60",
                    "סניף 70": "70"
                  },
                  "default": "סניף 30"
                }
              }
            },
            {
              "from": "driver.id",
              "to": "customFields.2",
              "func": {
                "func": "x => String(x)"
              }
            },
            {
              "from": "depot",
              "to": "shifts.0.start.location.address",
              "func": {
                "map": {
                  "options": {
                    "סניף 20": "צרעה, ישראל",
                    "סניף 30": "בארות יצחק, ישראל",
                    "סניף 60": "אזור תעשייה ציפורית",
                    "סניף 70": "באר שבע"
                  },
                  "default": ""
                }
              }
            },
            {
              "from": "depot",
              "to": "shifts.0.start.coordinate.latitude",
              "func": {
                "map": {
                  "options": {
                    "סניף 20": "31.76230",
                    "סניף 30": "32.04453",
                    "סניף 60": "32.76037",
                    "סניף 70": "31.22249"
                  },
                  "default": ""
                }
              }
            },
            {
              "from": "depot",
              "to": "shifts.0.start.coordinate.longtitude",
              "func": {
                "map": {
                  "options": {
                    "סניף 20": "34.97867",
                    "סניף 30": "34.9082",
                    "סניף 60": "35.31783",
                    "סניף 70": "34.80152"
                  },
                  "default": ""
                }
              }
            },
            {
              "from": "depot",
              "to": "shifts.0.end.location.address",
              "func": {
                "map": {
                  "options": {
                    "סניף 20": "צרעה, ישראל",
                    "סניף 30": "בארות יצחק, ישראל",
                    "סניף 60": "אזור תעשייה ציפורית",
                    "סניף 70": "באר שבע"
                  },
                  "default": ""
                }
              }
            },
            {
              "from": "depot",
              "to": "shifts.0.end.coordinate.latitude",
              "func": {
                "map": {
                  "options": {
                    "סניף 20": "31.76230",
                    "סניף 30": "32.04453",
                    "סניף 60": "32.76037",
                    "סניף 70": "31.22249"
                  },
                  "default": ""
                }
              }
            },
            {
              "from": "depot",
              "to": "shifts.0.end.coordinate.longtitude",
              "func": {
                "map": {
                  "options": {
                    "סניף 20": "34.97867",
                    "סניף 30": "34.9082",
                    "סניף 60": "35.31783",
                    "סניף 70": "34.80152"
                  },
                  "default": ""
                }
              }
            },
            {
              "to": "routeNumber",
              "default": 0
            },
            {
              "from": "truckId",
              "to": "associatedTruckId"
            },
            {
              "from": "customFields.1",
              "to": "segment",
              "func": {
                "func": "s => `נהג ${s}`"
              }
            }
          ],
          "name": "drivers-ERP",
          "dataFormat": "json",
          "dataPath": "data",
          "requiredDictionaries": []
        }
      ],
      "mergeConfig": {
        "propertiesMergeMap": {},
        "mergeMode": "ignoreAll"
      },
      "dataType": "drivers",
      "name": "drivers-ERP",
      "isLockEnabled": false
    }
  ],
  "forms": [
    {
      "actionName": "routeExporting",
      "transformers": [
        {
          "from": "trucks.0.customFields.2.value",
          "to": "truckId",
          "label": "מזהה משאית",
          "displayValue": "v => v",
          "type": "input",
          "injectAsIs": false
        },
        {
          "from": "trucks.0.customFields.0.value",
          "to": "truckGroupId",
          "label": "מזהה סוג ציוד משאית",
          "displayValue": "v => v",
          "type": "input",
          "injectAsIs": false
        },
        {
          "from": "trucks.0.customFields.1.value",
          "to": "rodnetBranch",
          "label": "סניף רודנט",
          "displayValue": "v => v",
          "type": "input",
          "injectAsIs": false
        },
        {
          "from": "route.deliveryDate",
          "to": "deliveryDate",
          "func": {
            "func": " (d) =>  { const date = new Date(d); date.setTime( date.getTime() + 4 * 60 * 60 * 1000 ); return date;}"
          },
          "label": "תאריך",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false
        },
        {
          "from": "drivers.0.customFields.2.value",
          "to": "driverId",
          "label": "מזהה נהג",
          "displayValue": "v => v",
          "type": "input",
          "injectAsIs": false
        },
        {
          "to": "visits",
          "label": "הזמנה",
          "type": "object",
          "injectAsIs": false
        },
        {
          "from": "groupItem.customFields.3.value",
          "to": "customerId",
          "label": "מזהה לקוח",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.customFields.6.value",
          "to": "companyNumber",
          "label": "מספר חברה",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.orderIds.0",
          "to": "orderNum",
          "label": "מזהה הזמנה",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.visitType",
          "to": "orderType",
          "func": {
            "func": "visitType => visitType === 'w2c' ? 'O': 'P'"
          },
          "label": "סוג",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.weight",
          "to": "weight",
          "func": {
            "func": "v => (parseFloat(v)).toFixed(3)"
          },
          "label": "משקל",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.volume",
          "to": "volume",
          "func": {
            "func": "v => (parseFloat(v)).toFixed(3)"
          },
          "label": "נפח",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.worth",
          "to": "worth",
          "func": {
            "func": "v => (parseFloat(v)).toFixed(2)"
          },
          "label": "תיבות",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.customFields.7.value",
          "to": "boxes",
          "label": "מספר תיבות",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.customFields.5.value",
          "to": "certNum",
          "label": "מספר תעודת משלוח",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.customFields.15.value",
          "to": "branch",
          "label": "סניף",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.customFields.8.value",
          "to": "status",
          "label": "סטטוס בורר אישור הזמנה",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.customFields.9.value",
          "to": "canceled",
          "label": "הזמנה מבוטלת",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.items.0.customFields.10.value",
          "to": "prio",
          "label": "דחיפות",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.path.dropoff.coordinate.latitude",
          "to": "north",
          "label": "קו אורך",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.path.dropoff.coordinate.longitude",
          "to": "east",
          "label": "קו רוחב",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        },
        {
          "from": "groupItem.routeIndex",
          "to": "routeIndex",
          "label": "מיקום במסלול",
          "displayValue": "v=>v",
          "type": "input",
          "injectAsIs": false,
          "toGroup": "visits"
        }
      ],
      "inputPreperation": {
        "prettyName": "export visits in route",
        "readings": [
          {
            "queryType": "read",
            "entryName": "plan",
            "multipleResults": false,
            "entityName": "plans",
            "filterMapping": {
              "id": "planId"
            },
            "options": {}
          },
          {
            "queryType": "read",
            "entryName": "route",
            "multipleResults": false,
            "entityName": "routes",
            "filterMapping": {
              "id": "routeId"
            },
            "options": {}
          },
          {
            "queryType": "read",
            "entryName": "visits",
            "multipleResults": true,
            "entityName": "visits",
            "filterMapping": {
              "planId": "planId"
            },
            "options": {}
          }
        ],
        "preprocessorTransformers": [
          {
            "from": "route.steps",
            "to": "visitIds",
            "func": {
              "func": "(steps) => Array.from(new Set(steps.reduce((ids, newStep) => [...ids, ...newStep.visitsIds], [])))"
            }
          },
          {
            "from": "visits",
            "to": "visits",
            "propertyFrom": "id",
            "comparerFrom": "visitIds"
          },
          {
            "from": [
              "route.steps",
              "visits"
            ],
            "to": "visits",
            "func": {
              "func": "(steps, visits) => {\n  const mappingMap = new Map();\n  \n  const roundSteps = [];\n  let currentRound = [];\n  \n  (steps || []).forEach(step => {\n    if (step.type === 'pickup') {\n      if (currentRound.length > 0) {\n        roundSteps.push(currentRound);\n        currentRound = [];\n      }\n    }\n    if (step.type === 'dropoff' && step.visitsIds?.length > 0) {\n      currentRound.push(step);\n    }\n  });\n  \n  if (currentRound.length > 0) {\n    roundSteps.push(currentRound);\n  }\n  \n  roundSteps.forEach((round, roundIndex) => {\n    let nextIndex = 1; // Reset index for each round\n    \n    round.forEach(step => {\n      step.visitsIds.forEach(visitId => {\n        mappingMap.set(visitId, {\n          roundIndex: roundIndex + 1,\n          routeIndex: nextIndex++\n        });\n      });\n    });\n  });\n  \n  visits.forEach(visit => {\n    const mapping = mappingMap.get(visit.id);\n    if (mapping) {\n      visit.roundIndex = mapping.roundIndex;\n      visit.routeIndex = mapping.routeIndex;\n    } else {\n      visit.roundIndex = -1;\n      visit.routeIndex = -1;\n    }\n  });\n  \n  return visits;\n}"
            }
          },
          {
            "from": [
              "route",
              "route.steps",
              "visits"
            ],
            "to": "visits",
            "func": {
              "func": "(route, steps, visits) => {\n    const updateCustomFieldsFromPackageId = (item) => {\n        if (!item.packageId)\n            return;\n\n        if (!item.customFields) {\n            item.customFields = [];\n        }\n\n        try {\n            const customFields = JSON.parse(item.packageId);\n            if (!customFields) {\n                return\n            }\n\n            //for each key in the customFields object create a custom field\n            Object.keys(customFields).forEach(key => {\n                const customField = item.customFields.find(cf => cf.id === key);\n                if (customField) {\n                    customField.value = customFields[key];\n                    return;\n                }\n\n                item.customFields.push({\n                    id: key,\n                    value: customFields[key]\n                });\n            });\n        } catch (e) {\n        }\n    };\n\n    const routeIndex = String(route.number + 1).padStart(2, '0');\n\n    const rounds = [];\n    let currentRound = [];\n    let lastWasDropoff = false;\n\n    //go over visits and remove items that are isActive false; if no items left remove the visit\n    //and remove the steps for that visit\n    const filteredVisits = visits.filter(visit => {\n        visit.items = visit.items.filter(item => item.isActive);\n        if (visit.items.length === 0) {\n            return false;\n        }\n        return true;\n    });\n\n    const filteredSteps = steps.filter(step =>\n        step.type === 'pickup' || step.type === 'dropoff' ||\n        filteredVisits.some(visit => step.visitsIds?.includes(visit.id))\n    );\n\n    filteredSteps.forEach(step => {\n        if (step.type === 'pickup') {\n            if (lastWasDropoff) {\n                if (currentRound.length > 0) {\n                    rounds.push(currentRound);\n                }\n                currentRound = [step];\n            } else {\n                currentRound.push(step);\n            }\n            lastWasDropoff = false;\n        } else {\n            currentRound.push(step);\n            lastWasDropoff = true;\n        }\n    });\n\n    if (currentRound.length > 0) {\n        rounds.push(currentRound);\n    }\n\n    const visitPositions = new Map();\n\n    rounds.forEach((round, roundIdx) => {\n        const roundIndex = String(roundIdx + 1).padStart(2, '0');\n        let visitIndex = 1;\n\n        round.filter(step => step.type === 'dropoff')\n            .forEach(step => {\n                step.visitsIds?.forEach(visitId => {\n                    if (!visitPositions.has(visitId)) {\n                        visitPositions.set(visitId, {\n                            roundIndex,\n                            visitIndex: String(visitIndex++).padStart(2, '0')\n                        });\n                    }\n                });\n            });\n    });\n\n    const orderVisits = [];\n    for (const visit of filteredVisits) {\n        if (visit.items.length < 2) {\n            updateCustomFieldsFromPackageId(visit.items[0]);\n            orderVisits.push(visit);\n            continue;\n        }\n\n        for (const item of visit.items) {\n            updateCustomFieldsFromPackageId(item);\n            const visitClone = { ...visit };\n            visitClone.weight = item.weight;\n            visitClone.volume = item.volume;\n\n            visitClone.items = [item];\n            visitClone.orderIds = [item.orderId];\n\n            orderVisits.push({ ...visitClone });\n        }\n    }\n\n\n    orderVisits.forEach(visit => {\n        const position = visitPositions.get(visit.id);\n        if (position) {\n            visit.fakeOrderIds = visit.orderIds.map(orderId =>\n                `${routeIndex}-${position.roundIndex}-${position.visitIndex}-${orderId}`\n            );\n        } else {\n            visit.fakeOrderIds = visit.orderIds.map(orderId =>\n                `${routeIndex}-00-00-${orderId}`\n            );\n        }\n    });\n\n    return orderVisits;\n}"
            }
          },
          {
            "from": "plan.trucks",
            "to": "trucks",
            "propertyFrom": "id",
            "comparerFrom": "route.truckId"
          },
          {
            "from": "plan.drivers",
            "to": "drivers",
            "propertyFrom": "id",
            "comparerFrom": "route.driverIds"
          },
          {
            "from": [
              "route",
              "visits",
              "trucks",
              "drivers",
              "extraData.plannerConfiguration.fleet.defaultFleetData"
            ],
            "to": "validateExport",
            "func": {
              "func": "(route, visits, trucks, drivers, defaultFleetData) => {\n  const failureReasons = [];\n  const formatErrorMessage = () => {\n    return failureReasons.join(\", \");\n  };\n\n  const getCustomField = (customFields, id) => {\n    return customFields?.filter((cf) => cf.id === id)?.[0]?.value ?? \"-\";\n  };\n\n  const checkForInvalidTrucksOrDrivers = (trucks, drivers) => {\n    let isValid = true;\n    if (!trucks?.length || trucks.find((t) => getCustomField(t.customFields, \"customFields.2\").length > 5)) {\n      failureReasons.push(\"נמצאו מסלולים ללא משאיות חוקיות\");\n      isValid = false;\n    }\n\n    if (!drivers?.length || drivers.find((d) => getCustomField(d.customFields, \"customFields.2\").length > 5)) {\n      failureReasons.push(\"נמצאו מסלולים ללא נהגים חוקיים\");\n      isValid = false;\n    }\n\n    if (!isValid) {\n      throw new Error(formatErrorMessage());\n    }\n  };\n\n  const checkForMatchingBranches = (trucks, drivers, visits) => {\n    //branchSet.add( visit?.customFields?.filter( cf => cf.id === 'customFields.1')?.[0]?.value ?? '-');\n    const branchSet = new Set();\n    if (trucks) {\n      for (const truck of trucks) {\n        branchSet.add(\n          truck?.customFields?.filter((cf) => cf.id === \"customFields.1\")?.[0]?.value?.replace(\"DPT\", \"\") ?? \"-\"\n        );\n      }\n    }\n\n    if (drivers) {\n      for (const driver of drivers) {\n        branchSet.add(\n          driver?.customFields?.filter((cf) => cf.id === \"customFields.1\")?.[0]?.value?.replace(\"DPT\", \"\") ?? \"-\"\n        );\n      }\n    }\n\n    if (branchSet.size !== 1) {\n      failureReasons.push(` ${[...branchSet]} ישנו חוסר תאימות בין סניף ההזמנות לבין המשאית או הנהג`);\n      throw new Error(formatErrorMessage());\n    }\n  };\n\n  const checkVisitsValidity = (visits) => {\n    for (const visit of visits) {\n      const doesntHasSystemCoordinates =\n        !visit?.path?.dropoff?.coordinate?.latitude || !visit?.path?.dropoff?.coordinate?.longitude;\n      const doesntHasCustomCoordinates = !getCustomField(visit.customFields, \"customFields.11\")?.includes(\",\");\n      if (doesntHasSystemCoordinates && doesntHasCustomCoordinates) {\n        const visitName = visit?.contactsInfo?.customer?.companyName ?? \"לא ידוע\";\n        failureReasons.push(`כתובת ללקוח ${visitName} לא תקינה`);\n        throw new Error(formatErrorMessage());\n      }\n\n        if (doesntHasSystemCoordinates) {\n            const latLngArray = getCustomField(visit.customFields, \"customFields.11\").split(\",\");\n            if (latLngArray.length !== 2 || isNaN(latLngArray[0]) || isNaN(latLngArray[1])) {\n                const visitName = visit?.contactsInfo?.customer?.companyName ?? \"לא ידוע\";\n                failureReasons.push(`כתובת ללקוח ${visitName} לא תקינה`);\n                throw new Error(formatErrorMessage());\n            }\n\n            visit.path.dropoff.coordinate = {\n                latitude: parseFloat(latLngArray[0]),\n                longitude: parseFloat(latLngArray[1])\n            };\n        }\n    }\n  };\n\n  const checkForRounds = (route) => {\n    return;\n    if (!route.steps?.length) {\n      failureReasons.push(\"לא נמצאו נקודות העמסה ופריקה\");\n      throw new Error(formatErrorMessage());\n    }\n\n    let shouldCheckForDropoff = false;\n    for (const step of route.steps) {\n      if (shouldCheckForDropoff && step.type === \"pickup\") {\n        failureReasons.push(\"נמצאה נקודת העמסה לאחר נקודת הפריקה\");\n        throw new Error(formatErrorMessage());\n      }\n\n      if (step.type === \"pickup\") {\n        continue;\n      }\n\n      if (!shouldCheckForDropoff && step.type === \"dropoff\") {\n        shouldCheckForDropoff = true;\n        continue;\n      }\n    }\n  };\n\n  const checkTruckCapacityLimits = (trucks, visits) => {\n    const toleranceFactor = 1.03; // 5% over limit allowed\n  \n    // Group visits by their round using the fakeOrderIds\n    const roundGroups = new Map();\n    \n    visits.forEach(visit => {\n      if (!visit.fakeOrderIds?.length) return;\n      \n      // Extract routeIndex and roundIndex from the first fakeOrderId\n      // Format is: routeIndex-roundIndex-visitIndex-orderId\n      const [routeIndex, roundIndex] = visit.fakeOrderIds[0].split('-');\n      const roundKey = `${routeIndex}-${roundIndex}`;\n      \n      if (!roundGroups.has(roundKey)) {\n        roundGroups.set(roundKey, []);\n      }\n      roundGroups.get(roundKey).push(visit);\n    });\n  \n    // Check each round separately\n    roundGroups.forEach((roundVisits, roundKey) => {\n      const [routeIndex, roundIndex] = roundKey.split('-');\n      \n      // Calculate totals for this round\n      const roundWeight = roundVisits.reduce((sum, visit) => sum + (visit.weight || 0), 0);\n      const roundVolume = roundVisits.reduce((sum, visit) => sum + (visit.volume || 0), 0);\n  \n      // Check if any truck has sufficient capacity for this round\n      const hasValidTruck = trucks.some(truck => {\n        const weightLimit = truck.maxWeight * toleranceFactor;\n        const volumeLimit = truck.maxVolume * toleranceFactor;\n        \n        return weightLimit >= roundWeight && volumeLimit >= roundVolume;\n      });\n  \n      if (!hasValidTruck) {\n        failureReasons.push(\n`נפח או משקל ההזמנות חורג מקיבולת המשאית`\n        );\n        throw new Error(formatErrorMessage());\n      }\n    });\n  };\n\n  const checkSalesBranch = (visits) => {\n    const invalidVisits = visits\n      .filter(visit => {\n        const salesBranch = visit.customFields?.find(cf => cf.id === \"customFields.15\")?.value;\n        \n        const isInvalid = salesBranch === null || salesBranch === undefined || salesBranch.trim() === \"\";\n        \n        return isInvalid;\n      })\n      .map(visit => ({\n        customerName: visit?.contactsInfo?.customer?.companyName ?? \"לא ידוע\",\n        routeNumber: visit?.fakeOrderIds?.[0]?.split('-')?.[0] ?? \"לא משוייך\"\n      }));\n  \n    if (invalidVisits.length > 0) {\n      const visitsList = invalidVisits\n        .map(v => `${v.customerName} (מסלול ${parseInt(v.routeNumber) || v.routeNumber})`)\n        .join(\", \");\n  \n      failureReasons.push(`נמצאו לקוחות ללא סניף מכירות: ${visitsList}`);\n      throw new Error(formatErrorMessage());\n    }\n  };  \n  \n  checkSalesBranch(visits);\n  checkForRounds(route);\n  checkForInvalidTrucksOrDrivers(trucks, drivers);\n  checkForMatchingBranches(trucks, drivers, visits);\n  checkTruckCapacityLimits(trucks, visits);\n  checkVisitsValidity(visits);\n\n  return \"OK\";\n}"
            }
          },
          {
            "from": "visits",
            "to": "group",
            "func": {
              "groupBy": "fakeOrderIds.0"
            },
            "groupBy": "fakeOrderIds.0"
          }
        ]
      },
      "requests": [
        {
          "body": {
            "func": "(data) => {\n  const RIGHT_ALIGNED_FIELDS = new Set([\n    \"ORDER_NUMBER\",\n    \"ROUTE_ID\",\n    \"LONGITUDE\",\n    \"LATITUDE\",\n    \"ROUTE_INDEX\",\n    \"TRUCK_CODE\",\n  ]);\n\n  const formatField = (value, length, fieldName) => {\n    const stringValue = String(value || \"\");\n    if (RIGHT_ALIGNED_FIELDS.has(fieldName)) {\n      // Right align: pad with spaces on the left\n      return \" \".repeat(Math.max(0, length - stringValue.length)) + stringValue;\n    } else {\n      // Left align: pad with spaces on the right\n      return stringValue + \" \".repeat(Math.max(0, length - stringValue.length));\n    }\n  };\n\n  const formatDate = (date, format) => {\n    const d = new Date(date);\n    if (format === \"DDMMYYYY\") {\n      return d.toLocaleDateString(\"en-GB\").replaceAll(\"/\", \"\");\n    }\n    if (format === \"YYYY-MM-DD\") {\n      return d.toLocaleDateString(\"en-GB\").split(\"/\").reverse().join(\"-\");\n    }\n    return \"\";\n  };\n\n  const formatCoordinate = (value) => {\n    return Number(value).toFixed(4).replace(\".\", \"\");\n  };\n\n  /**\n   * Field positions according to AS400 specification\n   * Each field is defined by its start position and length\n   */\n  const FIELDS = {\n    CUSTOMER_ID: { start: 1, length: 15 }, // Customer number (left-aligned)\n    COMPANY_NUMBER: { start: 16, length: 1 }, // Company number\n    ORDER_NUMBER: { start: 17, length: 10 }, // Order number (right-aligned)\n    ORDER_TYPE: { start: 27, length: 1 }, // Order type (P/O)\n    DELIVERY_DATE: { start: 28, length: 10 }, // Delivery date DDMMYYYY\n    WORTH: { start: 38, length: 16 }, // Sales boxes amount (right-aligned)\n    WEIGHT: { start: 54, length: 16 }, // Weight in kg (right-aligned)\n    VOLUME: { start: 70, length: 16 }, // Volume boxes (right-aligned)\n    BOXES: { start: 86, length: 16 }, // Quantity (right-aligned)\n    ORDER_STATUS: { start: 102, length: 22 }, // Order approval status (always 8)\n    CERT_NUMBER: { start: 124, length: 19 }, // Delivery note number\n    BRANCH: { start: 143, length: 14 }, // Sales branch code\n    STATUS: { start: 157, length: 1 }, // Order selector status\n    CANCELED: { start: 158, length: 1 }, // Canceled order flag\n    PRIORITY: { start: 159, length: 1 }, // Order priority\n    RESERVE: { start: 160, length: 399 }, // Reserved space\n    ROUTE_ID: { start: 500, length: 9 }, // Route ID (vehicle number)\n    SPERATOR_1: { start: 509, length: 1 }, // Separator\n    ROUTE_DATE: { start: 510, length: 10 }, // Route date YYYY-MM-DD\n    ROUTE_INDEX: { start: 520, length: 5 }, // Station number (right-aligned)\n    LONGITUDE: { start: 525, length: 10 }, // Longitude coordinate\n    LATITUDE: { start: 535, length: 10 }, // Latitude coordinate\n    DRIVER_CODE: { start: 545, length: 10 }, // Driver code\n    TRUCK_CODE: { start: 555, length: 10 }, // Truck code\n    RODNET_BRANCH: { start: 565, length: 10 }, // RODNET branch\n    DIST_BRANCH: { start: 575, length: 14 }, // Distribution branch\n  };\n\n  const createEmptyLine = (length) => \" \".repeat(length);\n\n  const setFieldInLine = (line, value, position, length, fieldName) => {\n    const formattedValue = formatField(value, length, fieldName);\n    return line.substring(0, position - 1) + formattedValue + line.substring(position - 1 + length);\n  };\n  2, 689;\n\n  const { truckId, truckGroupId, deliveryDate, driverId, visits, rodnetBranch } = data;\n  const lines = [];\n\n  for (const [idx, visit] of visits.entries()) {\n    const {\n      customerId,\n      companyNumber,\n      orderNum,\n      orderType,\n      worth,\n      weight,\n      volume,\n      boxes,\n      certNum,\n      branch,\n      status,\n      canceled,\n      prio,\n      north,\n      east,\n      routeIndex,\n    } = visit;\n\n    // Initialize empty line with maximum length\n    let line = createEmptyLine(585);\n\n    // Set each field in its absolute position\n    line = setFieldInLine(line, customerId, FIELDS.CUSTOMER_ID.start, FIELDS.CUSTOMER_ID.length, \"CUSTOMER_ID\");\n    line = setFieldInLine(\n      line,\n      companyNumber.slice(0, 1),\n      FIELDS.COMPANY_NUMBER.start,\n      FIELDS.COMPANY_NUMBER.length,\n      \"COMPANY_NUMBER\"\n    );\n    line = setFieldInLine(line, orderNum, FIELDS.ORDER_NUMBER.start, FIELDS.ORDER_NUMBER.length, \"ORDER_NUMBER\");\n    line = setFieldInLine(line, orderType, FIELDS.ORDER_TYPE.start, FIELDS.ORDER_TYPE.length, \"ORDER_TYPE\");\n    line = setFieldInLine(\n      line,\n      formatDate(deliveryDate, \"DDMMYYYY\"),\n      FIELDS.DELIVERY_DATE.start,\n      FIELDS.DELIVERY_DATE.length,\n      \"DELIVERY_DATE\"\n    );\n    line = setFieldInLine(line, parseFloat(worth).toFixed(2), FIELDS.WORTH.start, FIELDS.WORTH.length, \"WORTH\");\n    line = setFieldInLine(line, parseFloat(weight).toFixed(3), FIELDS.WEIGHT.start, FIELDS.WEIGHT.length, \"WEIGHT\");\n    line = setFieldInLine(line, parseFloat(volume).toFixed(3), FIELDS.VOLUME.start, FIELDS.VOLUME.length, \"VOLUME\");\n    line = setFieldInLine(line, parseFloat(boxes).toFixed(3), FIELDS.BOXES.start, FIELDS.BOXES.length, \"BOXES\");\n    line = setFieldInLine(line, \"8\", FIELDS.ORDER_STATUS.start, FIELDS.ORDER_STATUS.length, \"ORDER_STATUS\");\n    line = setFieldInLine(line, certNum, FIELDS.CERT_NUMBER.start, FIELDS.CERT_NUMBER.length, \"CERT_NUMBER\");\n    line = setFieldInLine(line, branch, FIELDS.BRANCH.start, FIELDS.BRANCH.length, \"BRANCH\");\n    line = setFieldInLine(line, status.slice(0, 1), FIELDS.STATUS.start, FIELDS.STATUS.length, \"STATUS\");\n    line = setFieldInLine(line, canceled || \" \", FIELDS.CANCELED.start, FIELDS.CANCELED.length, \"CANCELED\");\n    line = setFieldInLine(line, prio || \" \", FIELDS.PRIORITY.start, FIELDS.PRIORITY.length, \"PRIORITY\");\n    line = setFieldInLine(line, \"\", FIELDS.RESERVE.start, FIELDS.RESERVE.length, \"RESERVE\");\n    line = setFieldInLine(line, truckId, FIELDS.ROUTE_ID.start, FIELDS.ROUTE_ID.length, \"ROUTE_ID\");\n    line = setFieldInLine(line, \"1\", FIELDS.SPERATOR_1.start, FIELDS.SPERATOR_1.length, \"SPERATOR_1\");\n    line = setFieldInLine(\n      line,\n      formatDate(deliveryDate, \"YYYY-MM-DD\"),\n      FIELDS.ROUTE_DATE.start,\n      FIELDS.ROUTE_DATE.length,\n      \"ROUTE_DATE\"\n    );\n    line = setFieldInLine(line, String(routeIndex), FIELDS.ROUTE_INDEX.start, FIELDS.ROUTE_INDEX.length, \"ROUTE_INDEX\");\n    line = setFieldInLine(\n      line,\n      formatCoordinate(east) + \"E\",\n      FIELDS.LONGITUDE.start,\n      FIELDS.LONGITUDE.length,\n      \"LONGITUDE\"\n    );\n    line = setFieldInLine(\n      line,\n      formatCoordinate(north) + \"N\",\n      FIELDS.LATITUDE.start,\n      FIELDS.LATITUDE.length,\n      \"LATITUDE\"\n    );\n    line = setFieldInLine(line, driverId, FIELDS.DRIVER_CODE.start, FIELDS.DRIVER_CODE.length, \"DRIVER_CODE\");\n    line = setFieldInLine(line, truckId, FIELDS.TRUCK_CODE.start, FIELDS.TRUCK_CODE.length, \"TRUCK_CODE\");\n    line = setFieldInLine(\n      line,\n      `${rodnetBranch}`,\n      FIELDS.RODNET_BRANCH.start,\n      FIELDS.RODNET_BRANCH.length,\n      \"RODNET_BRANCH\"\n    );\n    line = setFieldInLine(line, truckGroupId, FIELDS.DIST_BRANCH.start, FIELDS.DIST_BRANCH.length, \"DIST_BRANCH\");\n\n    lines.push(line);\n  }\n\n  return lines.join(\"\\r\");\n}"
          },
          "batch": {
            "wrapper": "{{REQUESTS}}",
            "delimiter": "\n"
          },
          "dataEncoding": "win1255",
          "skipEncoding": false,
          "host": "files.getruck.co.il",
          "port": 22,
          "username": "develop",
          "password": "XW5p3qkaRB",
          "toDelete": false,
          "remotePath": {
            "func": "(...args) => { const thisTime = new Date(); const timestamp = `${thisTime.getFullYear()}${String(thisTime.getMonth() + 1).padStart(2, '0')}${String(thisTime.getDate()).padStart(2, '0')}_${String(thisTime.getHours()).padStart(2, '0')}${String(thisTime.getMinutes()).padStart(2, '0')}${String(thisTime.getSeconds()).padStart(2, '0')}`;  return `/public/sftp_exports/jafora/nissim/RNSHB_${args[0][0].category}_${timestamp}.TXT`}"
          }
        }
      ]
    },
    {
      "actionName": "deliveryAddressFieldUpdating",
      "transformers": [
        {
          "from": [
            "visit.items.0.customFields.3.value"
          ],
          "to": "externalId",
          "label": "מזהה לקוח",
          "type": "input",
          "injectAsIs": false
        },
        {
          "from": [
            "visit.items.0.customerName"
          ],
          "to": "name",
          "label": "שם לקוח",
          "type": "input",
          "injectAsIs": true
        },
        {
          "from": "visit.path.dropoff.address",
          "to": "address",
          "label": "כתובת",
          "type": "input",
          "injectAsIs": true
        },
        {
          "from": "extraData.city",
          "to": "city",
          "label": "עיר",
          "type": "input",
          "injectAsIs": true
        },
        {
          "from": "visit.path.dropoff.coordinate.latitude",
          "to": "addressLat",
          "label": "רוחב",
          "type": "input",
          "injectAsIs": false
        },
        {
          "from": "visit.path.dropoff.coordinate.longitude",
          "to": "addressLng",
          "label": "אורך",
          "type": "input",
          "injectAsIs": false
        }
      ],
      "inputPreperation": {
        "prettyName": "auto generated",
        "readings": [
          {
            "queryType": "read",
            "entryName": "plan",
            "multipleResults": false,
            "entityName": "plans",
            "filterMapping": {
              "id": "planId"
            },
            "options": {}
          },
          {
            "queryType": "read",
            "entryName": "visit",
            "multipleResults": false,
            "entityName": "visits",
            "filterMapping": {
              "id": "visitId"
            },
            "options": {}
          }
        ],
        "preprocessorTransformers": []
      },
      "requests": [
        {
          "body": {
            "func": "(data) => {const customerData = data; customerData.coordinateEncodingQuality = 'גיאו-קוד שניתן על ידי המשתמש'; delete customerData.category;  const query = {entityName:\"customer\", queryType: \"upsertBulk\", filterBy: \"externalId\", data:[{create: {...customerData}, update: {...customerData}}]};\nreturn JSON.stringify({companyId: \"EC661390fcydRgwMNKuDaRNYpP2fFa52\", query: [query]}); }"
          },
          "dataEncoding": "utf8",
          "skipEncoding": false,
          "endpoint": "https://webhook.site/8e0faa71-5cf5-4283-bccc-4a73cdab07d9",
          "method": "POST",
          "headers": {
            "Content-Type": "txt/plain"
          }
        }
      ],
      "errorMessagePaths": [
        "error.message",
        "FORM.InterfaceErrors.text"
      ]
    }
  ],
  "erp": {
    "sideEffects": [
      {
        "listenOn": [
          {
            "name": "sendMachinesCountToOmri shuf",
            "propertiesRequirements": {}
          }
        ],
        "preparations": [],
        "transactionItems": [
          {
            "action": {
              "requestConfig": {
                "body": "{}",
                "dataEncoding": "utf8",
                "skipEncoding": false,
                "endpoint": {
                  "func": "({machinesCount})=>  `https://www.waboxapp.com/api/send/chat?token=67a1381e56e74aa5de17e98ea7488e7e643ec8cb50e7f&uid=972504951951&to=972526886699&text=${String(machinesCount)}`"
                },
                "method": "post",
                "headers": {}
              }
            }
          }
        ]
      }
    ],
    "config": {
      "general": {
        "isRtl": true,
        "homePage": {
          "pluginName": "ERP"
        },
        "fallbackPage": {
          "pluginName": "ERP"
        }
      },
      "translations": {
        "general": {
          "charts": "דאשבורד",
          "hello_username": "שלום",
          "properties": {
            "name": "שם",
            "description": "תיאור",
            "address": "כתובת",
            "addressLat": "קו רוחב",
            "addressLng": "קו אורך",
            "addressLine1": "שורת כתובת 1",
            "city": "עיר",
            "coordinateEncodingQuality": "איכות קידוד קואורדינטות",
            "geocodeVerified": "אימות גיאוקוד",
            "timeWindowMultiplier": "מכפיל חלון זמן",
            "lastOrderDate": "תאריך הזמנה אחרון",
            "timeWindow": "חלון זמן",
            "maxTruckSize": "גודל משאית מקסימלי",
            "serviceTimeFactor": "מקדם זמן שירות",
            "isBase": "בסיס",
            "isNetwork": "רשת",
            "serviceTimeInfo": "תצורת זמן שירות",
            "totalServiceTime": "זמן שירות כולל",
            "phone": "טלפון",
            "terms": "תנאים",
            "license": "רישיון",
            "homeAddress": "כתובת בית",
            "homeLat": "קו רוחב בית",
            "homeLng": "קו אורך בית",
            "shift": "משמרת",
            "shiftStart": "התחלת משמרת",
            "shiftEnd": "סיום משמרת",
            "startTime": "התחלת משמרת",
            "endTime": "סיום משמרת",
            "isActive": "פעיל",
            "isMonitored": "במעקב",
            "hasBaseAccess": "אישור כניסה לבסיס",
            "hasKmgAccess": "אישור כניסה לקמג",
            "priority": "עדיפות",
            "workingArea": "אזור עבודה",
            "labels": "תגיות",
            "plate": "מספר רישוי",
            "lineId": "מספר קו",
            "maxWeight": "משקל מקסימלי",
            "maxVolume": "נפח מקסימלי",
            "length": "אורך",
            "width": "רוחב",
            "height": "גובה",
            "type": "סוג",
            "dailyFixedCost": "עלות קבועה יומית",
            "minuteCost": "עלות לדקה",
            "kmCost": "עלות לק״מ",
            "stopCost": "עלות עצירה",
            "depot": "מחסן",
            "date": "תאריך",
            "status": "סטטוס",
            "checkInTime": "זמן התייצבות",
            "driverId": "מזהה נהג",
            "truckId": "מזהה משאית",
            "id": "מזהה",
            "externalId": "מזהה חיצוני",
            "createdAt": "נוצר בתאריך",
            "updatedAt": "עודכן בתאריך",
            "comment": "הערות"
          },
          "datepicker": {
            "today": "היום",
            "allDates": "הכל",
            "tomorrow": "מחר",
            "thisWeek": "השבוע",
            "thisMonth": "החודש",
            "nextWeek": "שבוע הבא",
            "nextMonth": "חודש הבא"
          }
        },
        "Table": {
          "columnNames": {
            "Driver": {
              "externalId": "קוד עובד"
            },
            "externalId": "מזהה חיצוני",
            "addressLat": "קו רוחב",
            "addressLng": "קו אורך",
            "round": "סבב",
            "timeWindow": "חלון זמן",
            "maxTruckSize": "גודל משאית מקסימלי",
            "orders": "הזמנות",
            "orderId": "מזהה הזמנה",
            "warehouse": "מחסן",
            "lineId": "מזהה קו",
            "pallets": "משטחים",
            "deliveryDate": "תאריך משלוח",
            "customer": "לקוח",
            "truckId": "מזהה משאית",
            "plate": "מספר רישוי",
            "maxWeight": "משקל מקסימלי",
            "maxVolume": "נפח מקסימלי",
            "priority": "עדיפות",
            "dailyFixedCost": "עלות קבועה יומית",
            "minuteCost": "עלות לדקה",
            "kmCost": "עלות לקילומטר",
            "stopCost": "עלות עצירה",
            "size": "גודל",
            "driverId": "מזהה נהג",
            "phone": "טלפון",
            "routeId": "מזהה מסלול",
            "capabilities": "יכולות",
            "description": "תיאור",
            "drivers": "נהגים",
            "id": "מזהה",
            "createdAt": "נוצר בתאריך",
            "updatedAt": "עודכן בתאריך"
          },
          "footer": {
            "currentPosition": "מציג {{totalPresent}} מתוך {{totalCount}}, עמוד {{currentPage}} מתוך {{totalPages}}"
          }
        }
      },
      "plugin": {
        "jafora_generateDailyPlan": {
          "config": {
            "Driver": true,
            "Truck": true,
            "Shift": true
          }
        },
        "SendMessage": {
          "config": {
            "dictionary": {
              "modalHeader": "שליחת הודעה לנהג",
              "sendButtonTitle": "שליחה",
              "buttonTitle": "שליחת הודעה לנהג",
              "emptyTemplateName": "טקסט חופשי"
            },
            "templates": [
              {
                "id": "template",
                "name": "TEMPLATE 1",
                "data": [
                  {
                    "accessorKey": "name",
                    "title": "שם"
                  },
                  {
                    "accessorKey": "deliveryDate",
                    "title": "תאריך משלוח"
                  },
                  {
                    "accessorKey": "routeName",
                    "title": "שם המסלול"
                  }
                ],
                "func": "(templateData, drivers, routes) => { const driversText = drivers.map(driver => templateData.map(d => `${d.title}: ${driver[d.accessorKey]}`).join('\\n')).join('\\n\\n'); return `Generated message \\n\\n ${driversText}`; }"
              },
              {
                "id": "templateTwo",
                "name": "TEMPLATE 2",
                "data": [
                  {
                    "accessorKey": "name",
                    "title": "שם"
                  },
                  {
                    "accessorKey": "deliveryDate",
                    "title": "תאריך משלוח"
                  },
                  {
                    "accessorKey": "routeName",
                    "title": "שם המסלול"
                  }
                ],
                "func": "(templateData, drivers, routes) => { const driversText = drivers.map(driver => templateData.map(d => `${d.title}: ${driver[d.accessorKey]}`).join('\\n')).join('\\n\\n'); return `Generated message \\n\\n ${driversText}`; }"
              }
            ]
          }
        },
        "PieChart": {
          "config": {
            "RouteStatusRaw": {
              "title": "מסלולים לפי סטטוס",
              "dictionary": {
                "Initial": "טרם החל",
                "Inprogress": "בתהליך",
                "Done": "בוצע"
              },
              "xAxis": {
                "title": "Status",
                "field": "status"
              },
              "yAxis": {
                "title": "Routes",
                "field": "id"
              }
            },
            "DriverAvailability": {
              "title": "נהגים לפי חברת הובלה",
              "xAxis": {
                "title": "Company",
                "field": "shipperName"
              },
              "yAxis": {
                "title": "Company",
                "field": "shipperName"
              }
            }
          }
        },
        "GaugeChart": {
          "config": {
            "EstimatedDeliveryTWQualificationRaw": {
              "title": "רמת שירות צפויה - סניפים",
              "yAxis": {
                "title": "מצב נוכחי",
                "field": "results"
              }
            }
          }
        },
        "BarChart": {
          "config": {
            "DriverAvailability": {
              "title": "DriverAvailability",
              "xAxis": {
                "title": "License",
                "field": "license"
              },
              "yAxis": {
                "title": "Driver",
                "field": "-id"
              }
            }
          }
        },
        "List": {
          "config": {
            "Driver": {
              "numberOfItemsToRender": 5,
              "columns": [
                {
                  "id": "isActive",
                  "label": "פעיל",
                  "key": "isActive",
                  "transformFunction": "(v) => v ? 'פעיל':'לא פעיל'"
                },
                {
                  "id": "shipperName",
                  "label": "שם ספק",
                  "key": "shipperName"
                },
                {
                  "id": "shiftStart",
                  "label": "תחילת משמרת",
                  "key": "shiftStart"
                },
                {
                  "id": "shiftEnd",
                  "label": "סיום משמרת",
                  "key": "shiftEnd"
                },
                {
                  "id": "homeAddress",
                  "label": "מחסן מרכזי",
                  "key": "homeAddress"
                },
                {
                  "id": "truckPlate",
                  "label": "משאית",
                  "key": "truckPlate"
                },
                {
                  "id": "phone",
                  "label": "phone",
                  "key": "phone"
                },
                {
                  "id": "isMonitored",
                  "label": "isMonitored",
                  "transformFunction": "(v) => v ? '✅' : '❌'",
                  "key": "isMonitored"
                },
                {
                  "id": "routeMessages",
                  "label": "routeMessages",
                  "key": "routeMessages"
                },
                {
                  "id": "capabilities",
                  "label": "capabilities",
                  "key": "capabilities"
                },
                {
                  "id": "customersScores",
                  "label": "customersScores",
                  "key": "customersScores"
                },
                {
                  "id": "shift",
                  "label": "משמרת מועדפת",
                  "key": "shift"
                },
                {
                  "id": "license",
                  "label": "רשיון",
                  "key": "license"
                }
              ]
            }
          }
        },
        "Homepage": {
          "config": {
            "sections": [
              {
                "title": "אפליקציות ולינקים חיצונים",
                "applicationBlocks": [
                  {
                    "title": "מערכת תכנון",
                    "subtitle": "תכנון אופטימלי של קווי ההפצה",
                    "icon": "icon-map-paper",
                    "link": "/plannings"
                  },
                  {
                    "title": "מערכת ליקוט",
                    "subtitle": "מערכת WMS - ניהול מחסנים",
                    "icon": "icon-forklift",
                    "link": "/foklift"
                  },
                  {
                    "title": "פורטל דוחות",
                    "subtitle": "פורטל BI כלל אירגוני",
                    "icon": "icon-monitoring-dashboard",
                    "link": "/erp/erp?pageType=DASHBOARD&navigationGroup=default"
                  },
                  {
                    "title": "איתוראן",
                    "subtitle": "ניהול ציי רכב מבוססי מיקום",
                    "icon": "",
                    "link": "https://www.ituran.com/iweb2/"
                  }
                ]
              },
              {
                "title": "מודולי מערכת",
                "applicationBlocks": [
                  {
                    "title": "מכירות",
                    "subtitle": "ניהול מידע לקוחות",
                    "icon": "icon-map-paper",
                    "link": "/erp/Order"
                  },
                  {
                    "title": "תפעול והפצה",
                    "subtitle": "מערך הפצה ממשימה למסירה",
                    "icon": "icon-currency",
                    "link": "/erp/erp?pageType=LIST&schema=Route&navigationGroup=shuf"
                  },
                  {
                    "title": "ניהול צי",
                    "subtitle": "מצבת נהגים",
                    "icon": "",
                    "link": "/erp/erp?pageType=LIST&schema=Driver&navigationGroup=shuf"
                  },
                  {
                    "title": "רכב",
                    "subtitle": "ניהול מידע צי רכב נהגים",
                    "icon": "icon-local-shipping",
                    "link": "/erp/erp?pageType=LIST&schema=Truck&navigationGroup=shuf"
                  },
                  {
                    "title": "רכש",
                    "subtitle": "ניהול ספקים ומכרזים ",
                    "icon": "",
                    "link": "/erp/Shipper"
                  },
                  {
                    "title": "הנהלת חשבונות",
                    "subtitle": "מערכת ניהול ומעקב תשלומי לקוחות ספקים",
                    "icon": "icon-account-balance",
                    "link": "https://platform-prod.getruck.co.il/jupiter/control_room"
                  },
                  {
                    "title": "הגדרות",
                    "subtitle": "קבע את תצורת הפלטפורמה",
                    "icon": "icon-settings",
                    "link": "/config"
                  }
                ]
              }
            ]
          }
        },
        "Enrich": {
          "config": {
            "Point": {
              "enrichDataFields": {
                "times": {
                  "startTime": {
                    "accessorKey": "planTimeOfArrival",
                    "type": "timeString"
                  },
                  "endTime": {
                    "accessorKey": "endTime",
                    "type": "timeString"
                  }
                },
                "coordinates": {
                  "address": {
                    "accessorKey": "address"
                  }
                }
              },
              "allowDndFor": {
                "type": "Delivery"
              },
              "pinLast": {
                "type": "ShiftEnd"
              },
              "entityTitleKey": "name",
              "subfields": [
                {
                  "accessorKey": "address"
                },
                {
                  "accessorKey": "type"
                },
                {
                  "accessorKey": "planTimeOfArrival",
                  "position": "end"
                }
              ],
              "recalculateFields": [
                "planTimeOfArrival",
                "endTime",
                "startTime"
              ],
              "dictionary": {
                "title": "סדר מחדש נקודות",
                "buttonTitle": "סדר מחדש נקודות",
                "saveButton": "שמור",
                "closeButton": "בטל",
                "calculateButton": "חשב",
                "successNotificaton": "בוצע בהצלחה",
                "failureNotification": "משהו השתבש",
                "calculationSuccessNotification": "החישוב הצליח",
                "calculationFailureNotification": "החישוב נכשל"
              },
              "dataExtractionFunctions": {
                "getCoordinates": "(point) => [point.latitude, point.longitude].map(v => v ?? 1)"
              }
            }
          }
        },
        "ColumnChart": {
          "config": {
            "DriverAvailability": {
              "title": "מספר נהגים לפי רשיון",
              "xAxis": {
                "title": "רשיון",
                "field": "license",
                "hideLabels": false
              },
              "yAxis": {
                "title": "מספר נהגים",
                "field": "id",
                "hideLabels": true,
                "calculationType": "amount"
              }
            }
          }
        },
        "ColumnChart2": {
          "config": {
            "DriverAvailability": {
              "orientation": "horizontal",
              "title": "אורך משמרת נהגים",
              "chartBodyLabel": "(x, y) => { const hours = String(Math.floor(y / 60)); const minutes = String(y % 60); const preparedY = (hours.length === 1 ? '0' + hours : hours) + \":\" + (minutes.length === 1 ? '0' + minutes : minutes ); const preparedX = typeof x === 'string' ? x.slice(0, -11) : x; return '<b>' + preparedX + ',</b> ' + preparedY; }",
              "xAxis": {
                "title": "",
                "field": "id",
                "hideLabels": true,
                "labelValuePresenter": "(value) => { if (typeof value === 'string') { return value.slice(0, -11); } else { return value; } }"
              },
              "yAxis": {
                "title": "",
                "field": "routesStartingTime",
                "hideLabels": true,
                "calculationType": "sum",
                "hideZeroValues": false,
                "valueExtractor": "(value) => { if (typeof value !== \"string\") { return 0 }; const maybeTime = value.split(\":\"); if (typeof maybeTime[0] !== \"string\" || typeof maybeTime[1] !== \"string\") { return 0; }; const hours = Number(maybeTime[0]); const minutes = Number(maybeTime[1]); if (Number.isNaN(hours) || Number.isNaN(minutes)) { return 0; }; return hours * 60 + minutes; }",
                "labelValuePresenter": "(value) => { const hours = String(Math.floor(value / 60)); const minutes = String(value % 60); return (hours.length === 1 ? '0' + hours : hours) + \":\" + (minutes.length === 1 ? '0' + minutes : minutes )}"
              },
              "dataTransform": {
                "sort": "desc",
                "slice": [
                  [
                    0,
                    5
                  ],
                  [
                    -5
                  ]
                ]
              }
            }
          }
        },
        "ERP": {
          "config": {
            "general": {
              "navigationGroups": {
                "main": [
                  {
                    "pageType": "List",
                    "schema": "Shift",
                    "label": "צי לתכנון"
                  },
                  {
                    "pageType": "List",
                    "schema": "Customer",
                    "label": "לקוחות"
                  },
                  {
                    "label": "צי",
                    "items": [
                      {
                        "pageType": "List",
                        "schema": "Driver",
                        "label": "נהגים"
                      },
                      {
                        "pageType": "List",
                        "schema": "Truck",
                        "label": "משאיות"
                      }
                    ]
                  }
                ]
              }
            },
            "Shift": {
              "mainTablePageSize": 500,
              "detailsTablePageSize": 5,
              "title": "משמרת",
              "titlePlural": "משמרות",
              "fetchContinuously": 2000,
              "include": {
                "driver": true,
                "truck": true
              }
            },
            "Customer": {
              "mainTablePageSize": 1000,
              "detailsTablePageSize": 5,
              "title": "לקוח",
              "titlePlural": "לקוחות",
              "fetchContinuously": 2000,
              "include": {
                "serviceTime": true,
                "rawCustomer": true
              }
            },
            "Driver": {
              "mainTablePageSize": 500,
              "detailsTablePageSize": 5,
              "title": "נהג",
              "titlePlural": "נהגים",
              "fetchContinuously": 2000,
              "include": {
                "trucks": true,
                "truck": true,
                "shifts": true,
                "rawDriver": true
              }
            },
            "Truck": {
              "mainTablePageSize": 500,
              "detailsTablePageSize": 5,
              "title": "משאית",
              "titlePlural": "משאיות",
              "fetchContinuously": 2000,
              "include": {
                "drivers": true,
                "simpleDrivers": true,
                "shifts": true,
                "rawTruck": true
              }
            },
            "readonlyFields": [
              "updatedAt",
              "createdAt",
              "id",
              "routeId",
              "truckId",
              "orderId",
              "driverId",
              "driverName",
              "lineId",
              "shipperId",
              "operatorId",
              "pointsCount"
            ]
          }
        },
        "Table": {
          "config": {
            "Customer": {
              "filters": {
                "filterSpecificationToFilterTarget": {
                  "name": "name",
                  "description": "description",
                  "address": "address",
                  "city": "city",
                  "timeWindowMultiplier": "timeWindowMultiplier",
                  "serviceTimeFactor": "serviceTimeFactor",
                  "isBase": "isBase",
                  "isNetwork": "isNetwork",
                  "maxTruckSize": "maxTruckSize",
                  "externalId": "externalId",
                  "createdAt": "createdAt",
                  "updatedAt": "updatedAt"
                },
                "filterSpecifications": [
                  {
                    "name": "name",
                    "displayName": "שם לקוח",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "description",
                    "displayName": "תיאור",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "address",
                    "displayName": "כתובת",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "city",
                    "displayName": "עיר",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "isBase",
                    "displayName": "בסיס",
                    "multipleItems": false,
                    "dataType": "dropDown",
                    "functionNames": [
                      "equals"
                    ],
                    "values": "(rows)=> [{value: true, content: 'כן'}, {value: false, content: 'לא'}]"
                  },
                  {
                    "name": "isNetwork",
                    "displayName": "רשת",
                    "multipleItems": false,
                    "dataType": "dropDown",
                    "functionNames": [
                      "equals"
                    ],
                    "values": "(rows)=> [{value: true, content: 'כן'}, {value: false, content: 'לא'}]"
                  },
                  {
                    "name": "maxTruckSize",
                    "displayName": "גודל משאית מקסימלי",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "serviceTimeFactor",
                    "displayName": "מקדם זמן שירות",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  }
                ]
              },
              "download": {
                "format": [
                  "xlsx"
                ],
                "filename": "לקוחות"
              },
              "columns": [
                {
                  "id": "serviceTimeInfo",
                  "label": "Service Time Config",
                  "key": "serviceTimeInfo",
                  "columnWidth": 180
                },
                {
                  "id": "totalServiceTime",
                  "label": "Total Service Time",
                  "key": "totalServiceTime",
                  "columnWidth": 120,
                  "plugin": {
                    "name": "Text",
                    "props": {
                      "colorFn": "(value) => parseInt(value) > 120 ? 'red' : 'inherit'"
                    }
                  }
                },
                {
                  "id": "name",
                  "label": "Name",
                  "key": "name",
                  "columnWidth": 150
                },
                {
                  "id": "description",
                  "label": "Description",
                  "key": "description",
                  "columnWidth": 200
                },
                {
                  "id": "address",
                  "label": "Address",
                  "key": "address",
                  "columnWidth": 200
                },
                {
                  "id": "city",
                  "label": "City",
                  "key": "city",
                  "columnWidth": 120
                },
                {
                  "id": "addressLat",
                  "label": "Latitude",
                  "key": "addressLat",
                  "columnWidth": 100
                },
                {
                  "id": "addressLng",
                  "label": "Longitude",
                  "key": "addressLng",
                  "columnWidth": 100
                },
                {
                  "id": "timeWindow",
                  "label": "Time Window",
                  "key": "timeWindow",
                  "columnWidth": 120
                },
                {
                  "id": "maxTruckSize",
                  "label": "Max Truck Size",
                  "key": "maxTruckSize",
                  "columnWidth": 100
                },
                {
                  "id": "serviceTimeFactor",
                  "label": "Service Time Factor",
                  "key": "serviceTimeFactor",
                  "columnWidth": 120
                },
                {
                  "id": "isBase",
                  "label": "Is Base",
                  "key": "isBase",
                  "columnWidth": 80,
                  "transformFunction": "(isBase) => isBase ? '✅' : '' "
                },
                {
                  "id": "isNetwork",
                  "label": "Is Base",
                  "key": "isNetwork",
                  "columnWidth": 80,
                  "transformFunction": "(isNetwork) => isNetwork ? '✅' : '' "
                }
              ],
              "views": [
                {
                  "name": "הכל",
                  "columns": [
                    "name",
                    "description",
                    "address",
                    "city",
                    "isBase",
                    "isNetwork",
                    "externalId"
                  ]
                },
                {
                  "name": "גיאוגרפי",
                  "columns": [
                    "city",
                    "name",
                    "address",
                    "addressLat",
                    "addressLng"
                  ],
                  "sort": [
                    {
                      "property": "city",
                      "order": "asc"
                    }
                  ]
                },
                {
                  "name": "שירות",
                  "columns": [
                    "name",
                    "city",
                    "serviceTimeInfo",
                    "isBase",
                    "isNetwork"
                  ],
                  "sort": [
                    {
                      "property": "serviceTimeFactor",
                      "order": "desc"
                    }
                  ]
                }
              ],
              "rowsToShowPerPage": 50,
              "dictionary": {
                "entityTitle": "לקוח",
                "entityTitlePlural": "לקוחות",
                "id": "מזהה",
                "name": "שם",
                "description": "תיאור",
                "address": "כתובת",
                "city": "עיר",
                "addressLat": "קו רוחב",
                "addressLng": "קו אורך",
                "timeWindow": "חלון זמן",
                "maxTruckSize": "גודל משאית מקסימלי",
                "serviceTimeFactor": "מקדם זמן שירות",
                "serviceTimeInfo": "תצורת זמן שירות",
                "totalServiceTime": "זמן שירות כולל",
                "coordinateEncodingQuality": "איכות קידוד קואורדינטות",
                "geocodeVerified": "אימות גיאוקוד",
                "addressLine1": "שורת כתובת 1",
                "timeWindowMultiplier": "מכפיל חלון זמן",
                "isBase": "בסיס",
                "externalId": "מזהה חיצוני",
                "createdAt": "נוצר בתאריך",
                "updatedAt": "עודכן בתאריך"
              }
            },
            "Truck": {
              "filters": {
                "filterSpecificationToFilterTarget": {
                  "plate": "plate",
                  "lineId": "lineId",
                  "maxWeight": "maxWeight",
                  "maxVolume": "maxVolume",
                  "length": "length",
                  "width": "width",
                  "height": "height",
                  "size": "size",
                  "type": "type",
                  "priority": "priority",
                  "dailyFixedCost": "dailyFixedCost",
                  "minuteCost": "minuteCost",
                  "kmCost": "kmCost",
                  "stopCost": "stopCost",
                  "homeAddress": "homeAddress",
                  "isActive": "isActive",
                  "labels": "labels",
                  "drivers": "drivers",
                  "externalId": "externalId",
                  "id": "id",
                  "createdAt": "createdAt",
                  "updatedAt": "updatedAt"
                },
                "filterSpecifications": [
                  {
                    "name": "plate",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "lineId",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "maxWeight",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "maxVolume",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "length",
                    "multipleItems": false,
                    "dataType": "float",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "width",
                    "multipleItems": false,
                    "dataType": "float",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "height",
                    "multipleItems": false,
                    "dataType": "float",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "size",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "type",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "priority",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "dailyFixedCost",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "minuteCost",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "kmCost",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "stopCost",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "homeAddress",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "isActive",
                    "multipleItems": false,
                    "dataType": "dropDown",
                    "functionNames": [
                      "equals"
                    ],
                    "values": "(rows)=> [{value: true, content: 'כן'}, {value: false, content: 'לא'}]"
                  },
                  {
                    "name": "externalId",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "id",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "createdAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  },
                  {
                    "name": "updatedAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  }
                ]
              },
              "columns": [
                {
                  "defaultSize": "100",
                  "id": "plate",
                  "label": "plate",
                  "key": "plate"
                },
                {
                  "defaultSize": "100",
                  "id": "lineId",
                  "label": "lineId",
                  "key": "lineId"
                },
                {
                  "defaultSize": "100",
                  "id": "maxWeight",
                  "label": "maxWeight",
                  "key": "maxWeight"
                },
                {
                  "defaultSize": "100",
                  "id": "maxVolume",
                  "label": "maxVolume",
                  "key": "maxVolume"
                },
                {
                  "defaultSize": "100",
                  "id": "length",
                  "label": "length",
                  "key": "length"
                },
                {
                  "defaultSize": "100",
                  "id": "width",
                  "label": "width",
                  "key": "width"
                },
                {
                  "defaultSize": "100",
                  "id": "height",
                  "label": "height",
                  "key": "height"
                },
                {
                  "defaultSize": "100",
                  "id": "size",
                  "label": "size",
                  "key": "size"
                },
                {
                  "defaultSize": "100",
                  "id": "type",
                  "label": "סניף מוצא",
                  "key": "type"
                },
                {
                  "defaultSize": "100",
                  "id": "priority",
                  "label": "priority",
                  "key": "priority"
                },
                {
                  "defaultSize": "100",
                  "id": "dailyFixedCost",
                  "label": "dailyFixedCost",
                  "key": "dailyFixedCost"
                },
                {
                  "defaultSize": "100",
                  "id": "minuteCost",
                  "label": "minuteCost",
                  "key": "minuteCost"
                },
                {
                  "defaultSize": "100",
                  "id": "kmCost",
                  "label": "kmCost",
                  "key": "kmCost"
                },
                {
                  "defaultSize": "100",
                  "id": "stopCost",
                  "label": "stopCost",
                  "key": "stopCost"
                },
                {
                  "defaultSize": "100",
                  "id": "homeAddress",
                  "label": "homeAddress",
                  "key": "homeAddress"
                },
                {
                  "defaultSize": "100",
                  "id": "isActive",
                  "label": "פעילה",
                  "key": "isActive",
                  "transformFunction": "(v) => v ? 'פעילה':'לא פעילה'",
                  "plugin": {
                    "name": "Badge",
                    "props": {
                      "design": {
                        "לא פעילה": [
                          "#CA0F0F",
                          "white"
                        ],
                        "פעילה": [
                          "#00AA39",
                          "white"
                        ]
                      },
                      "options": {
                        "פעילה": "פעילה",
                        "לא פעילה": "לא פעילה"
                      }
                    }
                  }
                },
                {
                  "defaultSize": "100",
                  "id": "labels",
                  "label": "labels",
                  "key": "labels"
                },
                {
                  "defaultSize": "100",
                  "id": "drivers",
                  "label": "drivers",
                  "key": "drivers"
                },
                {
                  "defaultSize": "100",
                  "id": "externalId",
                  "label": "externalId",
                  "key": "externalId"
                },
                {
                  "defaultSize": "100",
                  "id": "id",
                  "label": "id",
                  "key": "id"
                },
                {
                  "defaultSize": "100",
                  "id": "createdAt",
                  "label": "createdAt",
                  "key": "createdAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                },
                {
                  "defaultSize": "100",
                  "id": "updatedAt",
                  "label": "updatedAt",
                  "key": "updatedAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                }
              ],
              "defaultColumnsWidth": 100,
              "views": [
                {
                  "name": "משאיות פעילות",
                  "columns": [
                    "plate",
                    "maxWeight",
                    "maxVolume",
                    "type",
                    "isActive",
                    "externalId"
                  ]
                },
                {
                  "name": "הכל",
                  "columns": [
                    "plate",
                    "lineId",
                    "maxWeight",
                    "maxVolume",
                    "length",
                    "width",
                    "height",
                    "size",
                    "type",
                    "priority",
                    "dailyFixedCost",
                    "minuteCost",
                    "kmCost",
                    "stopCost",
                    "homeAddress",
                    "isActive",
                    "labels",
                    "drivers",
                    "externalId",
                    "id",
                    "createdAt",
                    "updatedAt"
                  ]
                }
              ],
              "rowsToShowPerPage": 50,
              "groupBy": [
                {
                  "label": "plate",
                  "key": "plate"
                },
                {
                  "label": "lineId",
                  "key": "lineId"
                },
                {
                  "label": "maxWeight",
                  "key": "maxWeight"
                },
                {
                  "label": "maxVolume",
                  "key": "maxVolume"
                },
                {
                  "label": "length",
                  "key": "length"
                },
                {
                  "label": "width",
                  "key": "width"
                },
                {
                  "label": "height",
                  "key": "height"
                },
                {
                  "label": "size",
                  "key": "size"
                },
                {
                  "label": "type",
                  "key": "type"
                },
                {
                  "label": "priority",
                  "key": "priority"
                },
                {
                  "label": "dailyFixedCost",
                  "key": "dailyFixedCost"
                },
                {
                  "label": "minuteCost",
                  "key": "minuteCost"
                },
                {
                  "label": "kmCost",
                  "key": "kmCost"
                },
                {
                  "label": "stopCost",
                  "key": "stopCost"
                },
                {
                  "label": "homeAddress",
                  "key": "homeAddress"
                },
                {
                  "label": "isActive",
                  "key": "isActive"
                },
                {
                  "label": "labels",
                  "key": "labels"
                },
                {
                  "label": "drivers",
                  "key": "drivers"
                },
                {
                  "label": "externalId",
                  "key": "externalId"
                },
                {
                  "label": "id",
                  "key": "id"
                },
                {
                  "label": "createdAt",
                  "key": "createdAt"
                },
                {
                  "label": "updatedAt",
                  "key": "updatedAt"
                }
              ]
            },
            "Driver": {
              "overrideProperties": [
                "filters",
                "views"
              ],
              "filters": {
                "filterSpecificationToFilterTarget": {
                  "name": "name",
                  "phone": "phone",
                  "terms": "terms",
                  "license": "license",
                  "homeAddress": "homeAddress",
                  "homeLat": "homeLat",
                  "homeLng": "homeLng",
                  "shift": "shift",
                  "shiftStart": "shiftStart",
                  "shiftEnd": "shiftEnd",
                  "isActive": "isActive",
                  "isMonitored": "isMonitored",
                  "priority": "priority",
                  "workingArea": "workingArea",
                  "trucks": "trucks",
                  "externalId": "externalId",
                  "id": "id",
                  "createdAt": "createdAt",
                  "updatedAt": "updatedAt"
                },
                "filterSpecifications": [
                  {
                    "name": "name",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "phone",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "terms",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "license",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "homeAddress",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "homeLat",
                    "multipleItems": false,
                    "dataType": "float",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "homeLng",
                    "multipleItems": false,
                    "dataType": "float",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "shift",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "shiftStart",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "shiftEnd",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "isActive",
                    "multipleItems": false,
                    "dataType": "dropDown",
                    "functionNames": [
                      "equals"
                    ],
                    "values": "(rows)=> [{value: true, content: 'כן'}, {value: false, content: 'לא'}]"
                  },
                  {
                    "name": "isMonitored",
                    "multipleItems": false,
                    "dataType": "dropDown",
                    "functionNames": [
                      "equals"
                    ],
                    "values": "(rows)=> [{value: true, content: 'כן'}, {value: false, content: 'לא'}]"
                  },
                  {
                    "name": "priority",
                    "multipleItems": false,
                    "dataType": "int",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "externalId",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "id",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "createdAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  },
                  {
                    "name": "updatedAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  }
                ]
              },
              "columns": [
                {
                  "defaultSize": "100",
                  "id": "name",
                  "label": "name",
                  "key": "name"
                },
                {
                  "defaultSize": "100",
                  "id": "phone",
                  "label": "phone",
                  "key": "phone"
                },
                {
                  "defaultSize": "100",
                  "id": "terms",
                  "label": "terms",
                  "key": "terms"
                },
                {
                  "defaultSize": "100",
                  "id": "license",
                  "label": "license",
                  "key": "license"
                },
                {
                  "defaultSize": "100",
                  "id": "homeAddress",
                  "label": "homeAddress",
                  "key": "homeAddress"
                },
                {
                  "defaultSize": "100",
                  "id": "homeLat",
                  "label": "homeLat",
                  "key": "homeLat"
                },
                {
                  "defaultSize": "100",
                  "id": "homeLng",
                  "label": "homeLng",
                  "key": "homeLng"
                },
                {
                  "defaultSize": "100",
                  "id": "shift",
                  "label": "shift",
                  "key": "shift"
                },
                {
                  "defaultSize": "100",
                  "id": "shiftStart",
                  "label": "shiftStart",
                  "key": "shiftStart"
                },
                {
                  "defaultSize": "100",
                  "id": "shiftEnd",
                  "label": "shiftEnd",
                  "key": "shiftEnd"
                },
                {
                  "id": "isActive",
                  "label": "isActive",
                  "key": "isActive",
                  "transformFunction": "(v) => v ? 'פעיל':'לא פעיל'",
                  "plugin": {
                    "name": "Badge",
                    "props": {
                      "design": {
                        "לא פעיל": [
                          "#CA0F0F",
                          "white"
                        ],
                        "פעיל": [
                          "#00AA39",
                          "white"
                        ]
                      },
                      "options": {
                        "פעיל": "פעיל",
                        "לא פעיל": "לא פעיל"
                      }
                    }
                  }
                },
                {
                  "id": "hasBaseAccess",
                  "label": "א.כ לבסיס",
                  "key": "hasBaseAccess",
                  "transformFunction": "(v) => v ? '✅' : '' ",
                  "columnWidth": 120
                },
                {
                  "id": "hasKmgAccess",
                  "label": "hasKmgAccess",
                  "key": "hasKmgAccess",
                  "transformFunction": "(v) => v ? '✅' : '' ",
                  "columnWidth": 120
                },
                {
                  "defaultSize": "100",
                  "id": "isMonitored",
                  "label": "isMonitored",
                  "key": "isMonitored"
                },
                {
                  "defaultSize": "100",
                  "id": "priority",
                  "label": "priority",
                  "key": "priority"
                },
                {
                  "defaultSize": "100",
                  "id": "workingArea",
                  "label": "workingArea",
                  "key": "workingArea"
                },
                {
                  "defaultSize": "100",
                  "id": "trucks",
                  "label": "trucks",
                  "key": "trucks"
                },
                {
                  "defaultSize": "100",
                  "id": "truckPlate",
                  "label": "משאית",
                  "key": "truckPlate"
                },
                {
                  "defaultSize": "100",
                  "id": "externalId",
                  "label": "קוד עובד",
                  "key": "externalId"
                },
                {
                  "defaultSize": "100",
                  "id": "id",
                  "label": "id",
                  "key": "id"
                },
                {
                  "defaultSize": "100",
                  "id": "createdAt",
                  "label": "createdAt",
                  "key": "createdAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                },
                {
                  "defaultSize": "100",
                  "id": "updatedAt",
                  "label": "updatedAt",
                  "key": "updatedAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                }
              ],
              "defaultColumnsWidth": 100,
              "views": [
                {
                  "name": "כללי",
                  "columns": [
                    "externalId",
                    "name",
                    "truckPlate",
                    "shiftStart",
                    "shiftEnd",
                    "isActive",
                    "hasBaseAccess",
                    "hasKmgAccess"
                  ]
                }
              ],
              "rowsToShowPerPage": 50,
              "groupBy": [
                {
                  "label": "name",
                  "key": "name"
                },
                {
                  "label": "phone",
                  "key": "phone"
                },
                {
                  "label": "terms",
                  "key": "terms"
                },
                {
                  "label": "license",
                  "key": "license"
                },
                {
                  "label": "homeAddress",
                  "key": "homeAddress"
                },
                {
                  "label": "homeLat",
                  "key": "homeLat"
                },
                {
                  "label": "homeLng",
                  "key": "homeLng"
                },
                {
                  "label": "shift",
                  "key": "shift"
                },
                {
                  "label": "shiftStart",
                  "key": "shiftStart"
                },
                {
                  "label": "shiftEnd",
                  "key": "shiftEnd"
                },
                {
                  "label": "isActive",
                  "key": "isActive"
                },
                {
                  "label": "isMonitored",
                  "key": "isMonitored"
                },
                {
                  "label": "priority",
                  "key": "priority"
                },
                {
                  "label": "workingArea",
                  "key": "workingArea"
                },
                {
                  "label": "trucks",
                  "key": "trucks"
                },
                {
                  "label": "externalId",
                  "key": "externalId"
                },
                {
                  "label": "id",
                  "key": "id"
                },
                {
                  "label": "createdAt",
                  "key": "createdAt"
                },
                {
                  "label": "updatedAt",
                  "key": "updatedAt"
                }
              ],
              "slots": {
                "cell": {
                  "accessorKeys": [
                    "truckPlate"
                  ]
                }
              }
            },
            "DriverTruckScore": {
              "filters": {
                "filterSpecificationToFilterTarget": {
                  "score": "score",
                  "driverId": "driverId",
                  "driver": "driver",
                  "truckId": "truckId",
                  "truck": "truck",
                  "id": "id",
                  "createdAt": "createdAt",
                  "updatedAt": "updatedAt"
                },
                "filterSpecifications": [
                  {
                    "name": "score",
                    "multipleItems": false,
                    "dataType": "float",
                    "functionNames": [
                      "equals"
                    ]
                  },
                  {
                    "name": "driverId",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "truckId",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "id",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "createdAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  },
                  {
                    "name": "updatedAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  }
                ]
              },
              "columns": [
                {
                  "defaultSize": "100",
                  "id": "score",
                  "label": "score",
                  "key": "score"
                },
                {
                  "defaultSize": "100",
                  "id": "driverId",
                  "label": "driverId",
                  "key": "driverId"
                },
                {
                  "defaultSize": "100",
                  "id": "driver",
                  "label": "driver",
                  "key": "driver"
                },
                {
                  "defaultSize": "100",
                  "id": "truckId",
                  "label": "truckId",
                  "key": "truckId"
                },
                {
                  "defaultSize": "100",
                  "id": "truck",
                  "label": "truck",
                  "key": "truck"
                },
                {
                  "defaultSize": "100",
                  "id": "id",
                  "label": "id",
                  "key": "id"
                },
                {
                  "defaultSize": "100",
                  "id": "createdAt",
                  "label": "createdAt",
                  "key": "createdAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                },
                {
                  "defaultSize": "100",
                  "id": "updatedAt",
                  "label": "updatedAt",
                  "key": "updatedAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                }
              ],
              "defaultColumnsWidth": 100,
              "views": [
                {
                  "name": "הכל",
                  "columns": [
                    "score",
                    "driverId",
                    "driver",
                    "truckId",
                    "truck",
                    "id",
                    "createdAt",
                    "updatedAt"
                  ]
                }
              ],
              "rowsToShowPerPage": 50,
              "groupBy": [
                {
                  "label": "score",
                  "key": "score"
                },
                {
                  "label": "driverId",
                  "key": "driverId"
                },
                {
                  "label": "driver",
                  "key": "driver"
                },
                {
                  "label": "truckId",
                  "key": "truckId"
                },
                {
                  "label": "truck",
                  "key": "truck"
                },
                {
                  "label": "id",
                  "key": "id"
                },
                {
                  "label": "createdAt",
                  "key": "createdAt"
                },
                {
                  "label": "updatedAt",
                  "key": "updatedAt"
                }
              ]
            },
            "Shift": {
              "overrideProperties": [
                "filters",
                "views"
              ],
              "filters": {
                "filterSpecificationToFilterTarget": {
                  "date": "date",
                  "dateTomorrow": "date",
                  "dateToday": "date",
                  "status": "status",
                  "depot": "depot",
                  "checkInTime": "checkInTime",
                  "driverId": "driverId",
                  "driver": "driver",
                  "truckId": "truckId",
                  "truck": "truck",
                  "id": "id",
                  "createdAt": "createdAt",
                  "updatedAt": "updatedAt"
                },
                "filterSpecifications": [
                  {
                    "name": "dateTomorrow",
                    "displayName": "למחר",
                    "multipleItems": false,
                    "dataType": "dataless",
                    "functionNames": [
                      "datetime_tomorrow"
                    ]
                  },
                  {
                    "name": "dateToday",
                    "displayName": "להיום",
                    "multipleItems": false,
                    "dataType": "dataless",
                    "functionNames": [
                      "datetime_today"
                    ]
                  },
                  {
                    "name": "date",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  },
                  {
                    "name": "depot",
                    "displayName": "מחסן",
                    "multipleItems": true,
                    "dataType": "dropDown",
                    "functionNames": [
                      "contains"
                    ],
                    "values": "(rows) => [\n  { value: \"סניף 30\", content: \"סניף 30\" },\n  { value: \"סניף 20\", content: \"סניף 20\" },\n  { value: \"סניף 60\", content: \"סניף 60\" },\n  { value: \"סניף 70\", content: \"סניף 70\" }\n]"
                  },
                  {
                    "name": "status",
                    "displayName": "סטטוס",
                    "multipleItems": true,
                    "dataType": "multiSelect",
                    "functionNames": [
                      "contains"
                    ],
                    "values": "(rows) => [\n  { value: \"זמין\", content: \"זמין\" },\n  { value: \"לא זמין\", content: \"לא זמין\" }\n]"
                  },
                  {
                    "name": "checkInTime",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "driverId",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "id",
                    "multipleItems": false,
                    "dataType": "text",
                    "functionNames": [
                      "contains"
                    ]
                  },
                  {
                    "name": "createdAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  },
                  {
                    "name": "updatedAt",
                    "multipleItems": false,
                    "dataType": "date",
                    "functionNames": [
                      "datetime"
                    ]
                  }
                ]
              },
              "columns": [
                {
                  "defaultSize": "100",
                  "id": "date",
                  "label": "date",
                  "key": "date",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                },
                {
                  "id": "status",
                  "label": "סטטוס",
                  "key": "status",
                  "columnWidth": 120,
                  "plugin": {
                    "name": "Badge",
                    "props": {
                      "design": {
                        "זמין": [
                          "#00AA39",
                          "white"
                        ],
                        "לא זמין": [
                          "#CA0F0F",
                          "white"
                        ]
                      },
                      "options": {
                        "זמין": "זמין",
                        "לא זמין": "לא זמין"
                      }
                    }
                  }
                },
                {
                  "id": "depot",
                  "label": "מחסן",
                  "key": "depot",
                  "columnWidth": 120,
                  "plugin": {
                    "name": "Badge",
                    "props": {
                      "design": {
                        "סניף 30": [
                          "#90CDF4",
                          "black"
                        ],
                        "סניף 20": [
                          "#9AE6B4",
                          "black"
                        ],
                        "סניף 60": [
                          "#FEB2B2",
                          "black"
                        ],
                        "סניף 70": [
                          "#F6E05E",
                          "black"
                        ]
                      },
                      "options": {
                        "סניף 30": "סניף 30",
                        "סניף 20": "סניף 20",
                        "סניף 60": "סניף 60",
                        "סניף 70": "סניף 70"
                      }
                    }
                  }
                },
                {
                  "id": "driverName",
                  "label": "נהג",
                  "key": "driverName",
                  "columnWidth": 120
                },
                {
                  "id": "truckPlate",
                  "label": "משאית",
                  "key": "truckPlate",
                  "columnWidth": 100
                },
                {
                  "defaultSize": "100",
                  "id": "checkInTime",
                  "label": "checkInTime",
                  "key": "checkInTime"
                },
                {
                  "defaultSize": "100",
                  "id": "driverId",
                  "label": "driverId",
                  "key": "driverId"
                },
                {
                  "defaultSize": "100",
                  "id": "driver",
                  "label": "driver",
                  "key": "driver"
                },
                {
                  "defaultSize": "100",
                  "id": "id",
                  "label": "id",
                  "key": "id"
                },
                {
                  "defaultSize": "100",
                  "id": "createdAt",
                  "label": "createdAt",
                  "key": "createdAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                },
                {
                  "defaultSize": "100",
                  "id": "updatedAt",
                  "label": "updatedAt",
                  "key": "updatedAt",
                  "transformFunction": "(v) => v ? new Date(v).toLocaleDateString('en-GB') : ''"
                }
              ],
              "defaultColumnsWidth": 100,
              "views": [
                {
                  "name": "סניף 30",
                  "columns": [
                    "driverName",
                    "truckPlate",
                    "startTime",
                    "endTime",
                    "status",
                    "depot"
                  ],
                  "filters": [
                    {
                      "filterName": "depot",
                      "target": "depot",
                      "values": [
                        "סניף 30"
                      ]
                    }
                  ]
                },
                {
                  "name": "סניף 20",
                  "columns": [
                    "driverName",
                    "truckPlate",
                    "startTime",
                    "endTime",
                    "status",
                    "depot"
                  ],
                  "filters": [
                    {
                      "filterName": "depot",
                      "target": "depot",
                      "values": [
                        "סניף 20"
                      ]
                    }
                  ]
                },
                {
                  "name": "סניף 70",
                  "columns": [
                    "driverName",
                    "truckPlate",
                    "startTime",
                    "endTime",
                    "status",
                    "depot"
                  ],
                  "filters": [
                    {
                      "filterName": "depot",
                      "target": "depot",
                      "values": [
                        "סניף 70"
                      ]
                    }
                  ]
                },
                {
                  "name": "סניף 60",
                  "columns": [
                    "driverName",
                    "truckPlate",
                    "startTime",
                    "endTime",
                    "status",
                    "depot"
                  ],
                  "filters": [
                    {
                      "filterName": "depot",
                      "target": "depot",
                      "values": [
                        "סניף 60"
                      ]
                    }
                  ]
                }
              ],
              "rowsToShowPerPage": 50,
              "groupBy": [
                {
                  "label": "date",
                  "key": "date"
                },
                {
                  "label": "status",
                  "key": "status"
                },
                {
                  "label": "depot",
                  "key": "depot"
                },
                {
                  "label": "checkInTime",
                  "key": "checkInTime"
                },
                {
                  "label": "driverId",
                  "key": "driverId"
                },
                {
                  "label": "driver",
                  "key": "driver"
                },
                {
                  "label": "id",
                  "key": "id"
                },
                {
                  "label": "createdAt",
                  "key": "createdAt"
                },
                {
                  "label": "updatedAt",
                  "key": "updatedAt"
                }
              ],
              "slots": {
                "cell": {
                  "accessorKeys": [
                    "truckPlate"
                  ]
                }
              }
            }
          }
        },
        "TableBulkEdit": {
          "config": {
            "Tank": {
              "fields": [
                "type",
                "percThreshold",
                "fullTankWeight",
                "capacityUnits",
                "currentUnits",
                "currentPerc",
                "extraTanks",
                "comment",
                "fillPerDay",
                "softResetDate",
                "hardResetDate",
                "lastUpdateDate",
                "lastExtraTankUpdateDate",
                "machineId"
              ],
              "dictionary": {
                "type": "סוג מיכל",
                "percThreshold": "רף איסוף",
                "fullTankWeight": "משקל למיכל מלא (קג)",
                "capacityUnits": "קיבולת ביחידות",
                "currentUnits": "מספר בקבוקים במכונה",
                "currentPerc": "אחוז מילוי",
                "extraTanks": "מיכלים נוספים",
                "comment": "הערות",
                "fillPerDay": "קצב מילוי (קצב יומי)",
                "softResetDate": "תאריך איפוס Soft",
                "hardResetDate": "תאריך איפוס Hard",
                "lastUpdateDate": "תאריך עדכון אחרון",
                "lastExtraTankUpdateDate": "תאריך עדכון מיכל נוסף",
                "machineId": "מספר מכונה"
              }
            },
            "Machine": {
              "fields": [
                "isActive",
                "dataSource",
                "type",
                "calcMethod",
                "comment"
              ],
              "dictionary": {
                "isActive": "מכונה פעילה",
                "dataSource": "מקור נתונים",
                "type": "סוג מכונה",
                "calcMethod": "שיטת חישוב",
                "comment": "הערות"
              }
            },
            "CustomerSite": {
              "fields": [
                "siteId",
                "customerSiteId",
                "name",
                "customerName",
                "city",
                "address",
                "region",
                "latitude",
                "longitude",
                "isInBranch",
                "structureType",
                "isDaily",
                "comment"
              ],
              "dictionary": {
                "siteId": "מזהה סניף",
                "customerSiteId": "מספר לקוח",
                "name": "שם",
                "customerName": "שם לקוח",
                "city": "עיר",
                "address": "כתובת",
                "region": "אזור",
                "latitude": "קו רוחב",
                "longitude": "קו אורך",
                "isInBranch": "מכונה בתוך הסניף",
                "structureType": "סוג מבנה",
                "isDaily": "איסוף יומי",
                "comment": "הערות"
              }
            },
            "Truck": {
              "fields": [
                "size",
                "type",
                "homeAddress",
                "isActive",
                "kilometrage",
                "kilometrageUpdateDate",
                "licenseValidity",
                "insuranceValidity",
                "annualInspectionValidity",
                "semiAnnualInspectionValidity",
                "tachographInspectionValidity"
              ],
              "dictionary": {
                "homeAddress": "מרלוג מרכזי",
                "isActive": "פעילה",
                "kilometrage": "קילומטראז׳",
                "kilometrageUpdateDate": "ת.ע. קילומטרז׳",
                "licenseValidity": "רשיון",
                "insuranceValidity": "ביטוח",
                "annualInspectionValidity": "ב. שנתית",
                "semiAnnualInspectionValidity": "ב.ח. שנתית",
                "tachographInspectionValidity": "טכוגראף"
              }
            },
            "TruckAvailability": {
              "fields": [
                "truckType",
                "mainWarehouse",
                "date",
                "round4",
                "round1",
                "round2",
                "round3",
                "round8",
                "round6"
              ],
              "dictionary": {}
            },
            "DriverAvailability": {
              "fields": [
                "shift",
                "date",
                "round1",
                "round2",
                "round3",
                "round4",
                "round6",
                "round8"
              ],
              "dictionary": {
                "shift": "משמרת",
                "date": "תאריך",
                "round1": "סבב 1",
                "round2": "סבב 2",
                "round3": "סבב 3",
                "round4": "סבב 4",
                "round6": "סבב 6",
                "round8": "סבב 8"
              }
            },
            "Route": {
              "fields": [
                "name",
                "phone",
                "deliveryDate",
                "shiftStart",
                "shiftEnd"
              ],
              "dictionary": {
                "name": "שם",
                "phone": "טלפון",
                "deliveryDate": "תאריך",
                "shiftStart": "שעת תחילת משמרת",
                "shiftEnd": "שעת סיום משמרת"
              }
            },
            "Driver": {
              "fields": [
                "name",
                "phone",
                "isActive",
                "hasBaseAccess",
                "hasKmgAccess",
                "homeAddress",
                "shiftStart",
                "shiftEnd"
              ],
              "dictionary": {
                "name": "שם",
                "phone": "טלפון",
                "isActive": "פעיל",
                "hasBaseAccess": "אישור כניסה לבסיס",
                "hasKmgAccess": "אישור כניסה לקמג",
                "homeAddress": "כתובת",
                "shiftStart": "שעת תחילת משמרת",
                "shiftEnd": "שעת סיום משמרת"
              }
            },
            "Customer": {
              "fields": [
                "isBase",
                "isNetwork"
              ],
              "dictionary": {
                "isBase": "בסיס",
                "isNetwork": "רשת"
              }
            },
            "Shift": {
              "fields": [
                "status",
                "depot"
              ],
              "dictionary": {
                "status": "סטטוס",
                "depot": "מחסן"
              }
            }
          }
        },
        "EntityDetailsBlock": {
          "config": {
            "Shift": {
              "propertiesToRemove": [],
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "id",
                      "label": "מזהה",
                      "readonly": true
                    }
                  ]
                }
              ]
            },
            "Driver": {
              "propertiesToRemove": [],
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "id",
                      "label": "מזהה",
                      "readonly": true
                    }
                  ]
                }
              ]
            },
            "Truck": {
              "propertiesToRemove": [],
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "id",
                      "label": "מזהה",
                      "readonly": true
                    }
                  ]
                }
              ]
            },
            "Customer": {
              "propertiesToRemove": [],
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "id",
                      "label": "מזהה",
                      "readonly": true
                    }
                  ]
                }
              ]
            },
            "dictionary": {
              "saveAndContinue": "שמור והמשך",
              "save": "שמור",
              "cancel": "בטל",
              "dontSave": "המשך בלי לשמור",
              "confirmTitle": "לשמור שינויים?",
              "confirmMessage": "האם ברצונך לשמור את השינויים?",
              "notifyOnSave": "השינויים נשמרו בהצלחה",
              "notifyOnSaveError": "אירעה שגיאה בעת שמירת השינויים",
              "tryAgain": "נסה שוב"
            }
          }
        },
        "HeaderNavigation": {
          "config": {
            "Machine": {
              "titleFn": "(entityData)=> 'מכונה ' + entityData.machineId",
              "badgeLabel": "מכונה",
              "badgeColor": "#5da852"
            },
            "Route": {
              "titleFn": "(entityData)=> entityData.name",
              "badgeLabel": "מסלול",
              "badgeColor": "#5da852"
            },
            "Tank": {
              "titleFn": "(entityData)=> 'מיכל ' + entityData.type + ' - מכונה ' + entityData.machineId",
              "badgeLabel": "מיכל",
              "badgeColor": "#5da852"
            },
            "CustomerSite": {
              "titleFn": "(entityData)=> 'סניף ' + entityData.siteId + ' ' + entityData.name",
              "badgeLabel": "סניף",
              "badgeColor": "black"
            }
          }
        },
        "TableSummary": {
          "config": {
            "Mission": [
              {
                "label": "נבחרו",
                "icon": "check",
                "func": "(rawData) => rawData.length"
              }
            ]
          }
        },
        "PageTabBar": {
          "config": {
            "maxAmountToShow": 7,
            "mapIdToLabel": {
              "general": "כללי",
              "Customer": "לקוח"
            }
          }
        },
        "BlockEntityList": {
          "config": {
            "Driver": {
              "dictionary": {
                "name": "שם",
                "externalId": "מספר",
                "phone": "טלפון"
              },
              "fields": [
                "name",
                "externalId"
              ]
            },
            "Truck": {
              "dictionary": {
                "externalId": "מספר",
                "maxWeight": "משקל",
                "maxVolume": "נפח",
                "type": "סוג"
              },
              "fields": [
                "externalId",
                "type"
              ]
            }
          }
        },
        "GenerateQR": {
          "config": {}
        },
        "HeaderSecondary": {
          "config": {}
        },
        "CreateEntity": {
          "config": {
            "dictionary": {
              "saveAndContinue": "שמור והמשך",
              "save": "שמור",
              "cancel": "בטל",
              "dontSave": "המשך בלי לשמור",
              "confirmTitle": "לשמור שינויים?",
              "confirmMessage": "האם ברצונך לשמור את השינויים?",
              "notifyOnSave": "השינויים נשמרו בהצלחה",
              "notifyOnSaveError": "אירעה שגיאה בעת שמירת השינויים",
              "notifyOnAssign": "השיוך בוצע בהצלחה!",
              "notifyOnAssignError": "אירעה שגיאה בעת יצירת השיוך",
              "tryAgain": "נסה שוב",
              "create": "צור",
              "assign": "שייך"
            },
            "Driver": {
              "title": "צור נהג חדש",
              "assignTitle": "שייך נהג קיים",
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "name",
                      "label": "שם"
                    },
                    {
                      "key": "phone",
                      "label": "טלפון"
                    },
                    {
                      "label": "מחסן מרכזי",
                      "key": "homeAddress"
                    },
                    {
                      "label": "משמרת מועדפת",
                      "key": "shift"
                    },
                    {
                      "label": "רשיון",
                      "key": "license"
                    }
                  ]
                }
              ]
            },
            "DriverTimeOff": {
              "title": "צור אירוע",
              "assignTitle": "-",
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "driverId",
                      "label": "נהג"
                    },
                    {
                      "key": "dateStart",
                      "label": "מתאריך",
                      "size": "half"
                    },
                    {
                      "key": "dateEnd",
                      "label": "עד תאריך",
                      "size": "half"
                    },
                    {
                      "label": "סוג",
                      "key": "type"
                    },
                    {
                      "label": "הערות",
                      "key": "comment"
                    }
                  ]
                }
              ]
            },
            "Point": {
              "title": "צור נקודה חדשה",
              "assignTitle": "שייך נקודה קיימת",
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "name",
                      "label": "שם"
                    },
                    {
                      "key": "address",
                      "label": "כתובת"
                    },
                    {
                      "key": "type",
                      "label": "סוג",
                      "optionTranslations": {
                        "Pickup": "העמסה",
                        "Delivery": "פריקה",
                        "ShiftStart": "התחלת משמרת"
                      }
                    },
                    {
                      "key": "startTime",
                      "label": "זמן התחלה"
                    },
                    {
                      "key": "endTime",
                      "label": "זמן סיום"
                    },
                    {
                      "key": "planTimeOfArrival",
                      "label": "זמן צפוי"
                    },
                    {
                      "key": "comment",
                      "label": "הערה"
                    }
                  ]
                }
              ]
            },
            "Truck": {
              "title": "צור משאית חדשה",
              "assignTitle": "שייך משאית קיימת",
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "plate",
                      "label": "לוחית רישוי"
                    },
                    {
                      "key": "type",
                      "label": "סוג",
                      "optionTranslations": {
                        "8": "8",
                        "10": "10",
                        "12": "12",
                        "16": "16",
                        "20": "20",
                        "24": "24",
                        "20T": "20T",
                        "24T": "24T"
                      }
                    },
                    {
                      "key": "size",
                      "label": "גודל"
                    },
                    {
                      "key": "homeAddress",
                      "label": "מחסן מרכזי"
                    }
                  ]
                }
              ]
            },
            "CustomerSite": {
              "title": "צור סניף חדש",
              "assignTitle": "שייך סניף קיים",
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "siteId",
                      "label": "מזהה סניף",
                      "readonly": true
                    },
                    {
                      "key": "name",
                      "label": "שם סניף"
                    },
                    {
                      "key": "customerName",
                      "label": "שם לקוח"
                    }
                  ]
                },
                {
                  "label": "מיקום",
                  "properties": [
                    {
                      "key": "city",
                      "label": "עיר"
                    },
                    {
                      "key": "address",
                      "label": "כתובת"
                    },
                    {
                      "key": "latitude",
                      "label": "קו רוחב"
                    },
                    {
                      "key": "longitude",
                      "label": "קו אורך"
                    }
                  ]
                },
                {
                  "label": "פרטים",
                  "properties": [
                    {
                      "key": "region",
                      "label": "אזור לפי קו חלוקה"
                    },
                    {
                      "key": "isInBranch",
                      "label": "מכונה בתוך הסניף"
                    },
                    {
                      "key": "structureType",
                      "label": "סוג מבנה"
                    },
                    {
                      "key": "isDaily",
                      "label": "איסוף יומי"
                    },
                    {
                      "key": "comment",
                      "label": "הערה"
                    }
                  ]
                }
              ]
            }
          }
        },
        "shufersal_createPoint": {
          "config": {
            "dictionary": {
              "saveAndContinue": "שמור והמשך",
              "save": "שמור",
              "cancel": "בטל",
              "dontSave": "המשך בלי לשמור",
              "confirmTitle": "לשמור שינויים?",
              "confirmMessage": "האם ברצונך לשמור את השינויים?",
              "notifyOnSave": "השינויים נשמרו בהצלחה",
              "notifyOnSaveError": "אירעה שגיאה בעת שמירת השינויים",
              "notifyOnAssign": "השיוך בוצע בהצלחה!",
              "notifyOnAssignError": "אירעה שגיאה בעת יצירת השיוך",
              "tryAgain": "נסה שוב",
              "create": "צור",
              "assign": "שייך"
            },
            "Point": {
              "entityDataBlocks": [
                {
                  "label": "כללי",
                  "properties": [
                    {
                      "key": "name",
                      "label": "שם"
                    },
                    {
                      "key": "address",
                      "label": "כתובת"
                    },
                    {
                      "key": "type",
                      "label": "סוג",
                      "optionTranslations": {
                        "Pickup": "העמסה",
                        "Delivery": "פריקה",
                        "ShiftStart": "התחלת משמרת"
                      }
                    },
                    {
                      "key": "comment",
                      "label": "הערה"
                    }
                  ]
                }
              ]
            }
          }
        },
        "openDriverApp": {
          "config": {
            "Route": true
          }
        },
        "generateDailyPlan": {
          "config": {}
        },
        "importPlanFile": {
          "config": {}
        },
        "EntityRelationSelect": {
          "config": {
            "CustomerSite": {
              "dictionary": {
                "name": "שם סניף",
                "address": "כתובת",
                "city": "עיר",
                "customerName": "שם לקוח"
              },
              "fields": [
                "name",
                "address",
                "city",
                "customerName"
              ]
            },
            "Machine": {
              "dictionary": {
                "machineId": "מספר מכונה"
              },
              "fields": [
                "machineId"
              ]
            },
            "Tank": {
              "propToDisplay": "machineId",
              "dictionary": {
                "machineId": "מספר מכונה"
              },
              "fields": [
                "machineId"
              ]
            }
          }
        },
        "OpenDetailsView": {
          "config": {
            "dictionary": {
              "open": "פתח"
            }
          }
        }
      },
      "schemas": [
        {
          "id": "Shift",
          "type": "Physical",
          "calculatePropertyFunctions": {
            "truckPlate": "(data) => data?.truck?.plate"
          },
          "searchableFields": [
            "driverName"
          ],
          "dbTableName": "shifts"
        },
        {
          "id": "Customer",
          "type": "Physical",
          "aggregationFunctions": {},
          "calculatePropertyFunctions": {
            "serviceTimeInfo": "(data) => data?.serviceTime ? `${data.serviceTime.name} (${data.serviceTime.constantFactor || 0} + ${data.serviceTime.variableFactor || 0}x)` : ''",
            "totalServiceTime": "(data) => { if (!data.serviceTime) return null; const constant = data.serviceTime.constantFactor || 0; const variable = data.serviceTime.variableFactor || 0; const factor = data.serviceTimeFactor || 1; return Math.round((constant + variable) * factor); }"
          },
          "searchableFields": [
            "name",
            "description",
            "address",
            "city",
            "externalId"
          ],
          "dbTableName": "customers"
        },
        {
          "id": "Driver",
          "type": "Physical",
          "aggregationFunctions": {},
          "calculatePropertyFunctions": {
            "truckPlate": "(data) => data?.truck?.plate"
          },
          "searchableFields": [
            "name"
          ],
          "dbTableName": "drivers"
        },
        {
          "id": "Truck",
          "type": "Physical",
          "aggregationFunctions": {},
          "calculatePropertyFunctions": {},
          "searchableFields": [
            "externalId",
            "type",
            "plate"
          ],
          "dbTableName": "trucks"
        }
      ]
    }
  },
  "generalFuncs": {
    "deliveryDurationFunc": {
      "func": "(...items) => {\n      const serviceType = items[0].customFields[13].value;\n\n      const constantFactor = serviceType === \"PRATI\" ? 15 : 15;\n      const variableFactor = serviceType === \"PRATI\" ? 0.1 : 0.15;\n\n      const resultByFormula =\n        constantFactor +\n        Math.round(items.filter((item) => item.isActive).reduce((sum, it) => sum + variableFactor * it.worth, 0));\n\n      const maxServiceTime = 60;\n\n      return Math.min(resultByFormula, maxServiceTime);\n    }"
    },
    "warehouseDurationFunc": {
      "func": "(group) => { return group.steps.reduce((duration,s) => group.groupIndex == 0 ? Math.max(duration, s.step.duration) : 45, 0) }"
    }
  },
  "appsConfig": {
    "planner": {
      "appId": "planner",
      "customFields": [
        {
          "target": "Task",
          "title": "Tags",
          "type": "string",
          "values": [],
          "id": "customFields.0"
        },
        {
          "target": "Task",
          "title": "סניף",
          "type": "dropdown",
          "values": [],
          "id": "customFields.1"
        },
        {
          "target": "Task",
          "title": "חלון זמן",
          "type": "dropdown",
          "values": [],
          "id": "customFields.2"
        },
        {
          "target": "Task",
          "title": "מזהה לקוח",
          "type": "text",
          "values": [],
          "id": "customFields.3"
        },
        {
          "target": "LineInOrder",
          "title": "מס׳ הזמנה",
          "type": "text",
          "values": [],
          "id": "customFields.4"
        },
        {
          "target": "LineInOrder",
          "title": "תעודת משלוח",
          "type": "text",
          "values": [],
          "id": "customFields.5"
        },
        {
          "target": "Task",
          "title": "מספר חברה",
          "type": "text",
          "values": [],
          "id": "customFields.6"
        },
        {
          "target": "LineInOrder",
          "title": "תיבות (תקן)",
          "type": "text",
          "values": [],
          "id": "customFields.7"
        },
        {
          "target": "LineInOrder",
          "title": "סטטוס בורר הזמנה",
          "type": "text",
          "values": [],
          "id": "customFields.8"
        },
        {
          "target": "LineInOrder",
          "title": "הזמנה מבוטלת",
          "type": "text",
          "values": [],
          "id": "customFields.9"
        },
        {
          "target": "LineInOrder",
          "title": "דחיפות הזמנה",
          "type": "text",
          "values": [],
          "id": "customFields.10"
        },
        {
          "target": "Task",
          "title": "קואורדינטות",
          "type": "text",
          "values": [],
          "id": "customFields.11"
        },
        {
          "target": "Task",
          "title": "זמני ביקור",
          "type": "text",
          "values": [],
          "id": "customFields.12"
        },
        {
          "target": "Task",
          "title": "סוג זמן שירות",
          "type": "dropdown",
          "values": [],
          "id": "customFields.13"
        },
        {
          "target": "Task",
          "title": "האם רשת",
          "type": "dropdown",
          "values": [
            "כן",
            "לא"
          ],
          "id": "customFields.14"
        },
        {
          "target": "Task",
          "title": "סניף מכירה",
          "id": "customFields.15",
          "type": "dropdown",
          "values": [
            "20",
            "60",
            "70",
            "30"
          ]
        }
      ],
      "tableFields": [
        {
          "title": "תעודת משלוח",
          "key": "customFields.5",
          "visible": true,
          "editable": false
        },
        {
          "title": "מספר הזמנה",
          "key": "customFields.4",
          "visible": true,
          "editable": false
        },
        {
          "title": "משקל",
          "key": "weight",
          "visible": true,
          "editable": false
        },
        {
          "title": "נפח",
          "key": "volume",
          "visible": true,
          "editable": false
        },
        {
          "title": "מספר תיבות",
          "key": "worth",
          "visible": true,
          "editable": false
        },
        {
          "title": "סוג זמן שירות",
          "key": "customFields.13",
          "visible": true,
          "editable": false,
          "erpExportAction": ""
        }
      ],
      "routeInfo": {
        "header": {
          "secondaryField1": "driversNames",
          "primaryField": "truckPlateNumber",
          "secondaryField2": "truckMaxWeightAndVolume"
        }
      },
      "taskHeaderFields": [
        {
          "title": "pickupAddress",
          "key": "pickupAddress",
          "visible": true,
          "editable": true,
          "erpExportAction": ""
        },
        {
          "title": "deliveryAddress",
          "key": "deliveryAddress",
          "visible": true,
          "editable": true,
          "erpExportAction": "deliveryAddressFieldUpdating"
        },
        {
          "title": "companyName",
          "key": "contactsInfo.companyName",
          "visible": true,
          "editable": true,
          "erpExportAction": ""
        },
        {
          "title": "מזהה לקוח",
          "key": "customFields.3",
          "visible": true,
          "editable": false,
          "erpExportAction": ""
        },
        {
          "title": "contact",
          "key": "contactsInfo.contactName",
          "visible": false,
          "editable": true,
          "erpExportAction": ""
        },
        {
          "title": "deliveryDate",
          "key": "deliveryDates",
          "visible": true,
          "editable": true,
          "erpExportAction": ""
        },
        {
          "title": "contactPhone",
          "key": "contactsInfo.contactPhone",
          "visible": false,
          "editable": true,
          "erpExportAction": ""
        },
        {
          "title": "סניף",
          "key": "customFields.1",
          "visible": true,
          "editable": false,
          "erpExportAction": ""
        },
        {
          "title": "חלון זמן",
          "key": "customFields.2",
          "visible": true,
          "editable": false,
          "erpExportAction": ""
        },
        {
          "title": "קואורדינטות",
          "id": "customFields.11",
          "visible": false,
          "editable": false,
          "erpExportAction": ""
        },
        {
          "title": "זמני ביקור",
          "key": "customFields.12",
          "visible": true,
          "editable": false,
          "erpExportAction": ""
        },
        {
          "title": "סוג שירות",
          "key": "customFields.13",
          "visible": true,
          "editable": false,
          "erpExportAction": ""
        },
        {
          "title": "האם רשת",
          "key": "customFields.14",
          "visible": true,
          "editable": false,
          "erpExportAction": ""
        },
        {
          "title": "סניף מכירה",
          "key": "customFields.15",
          "visible": true,
          "editable": true,
          "erpExportAction": ""
        }
      ],
      "routeFilter": {
        "filterSpecificationToFilterTarget": {
          "truck.customFields.0": "__ROOT__",
          "truck.customFields.1": "__ROOT__",
          "truck.customFields.2": "__ROOT__",
          "truck.customFields.3": "__ROOT__",
          "truck.customFields.4": "__ROOT__"
        },
        "appendToDefaultFilters": true,
        "filterSpecifications": [
          {
            "name": "truck.customFields.0",
            "displayName": "קבוצת משאית",
            "multipleItems": true,
            "dataType": "multiselect",
            "functionNames": [
              "customFieldsContainSomeArray"
            ],
            "valuesSource": "truckCustomFieldValuesPrepared('customFields.0')"
          },
          {
            "name": "truck.customFields.1",
            "displayName": "מרלוג רכב",
            "multipleItems": true,
            "dataType": "multiselect",
            "functionNames": [
              "customFieldsContainSomeArray"
            ],
            "valuesSource": "truckCustomFieldValuesPrepared('customFields.1')"
          },
          {
            "name": "truck.customFields.2",
            "displayName": "מספר רכב",
            "multipleItems": true,
            "dataType": "multiselect",
            "functionNames": [
              "customFieldsContainSomeArray"
            ],
            "valuesSource": "truckCustomFieldValuesPrepared('customFields.2')"
          },
          {
            "name": "truck.customFields.3",
            "displayName": "סוג רכב",
            "multipleItems": true,
            "dataType": "multiselect",
            "functionNames": [
              "customFieldsContainSomeArray"
            ],
            "valuesSource": "truckCustomFieldValuesPrepared('customFields.3')"
          }
        ]
      },
      "route": {
        "showFirstWarehouse": true,
        "showDriverHome": true,
        "defaultNumberOfRoutes": 0,
        "tabs": {
          "board": {
            "visible": true,
            "isDefault": false
          },
          "details": {
            "visible": true,
            "isDefault": false
          },
          "summary": {
            "visible": true,
            "isDefault": true
          }
        }
      },
      "scheduling": {
        "isSchedulingRequired": false,
        "hideSchedulingInTaskEditor": true,
        "hideSchedulingContextMenu": true
      },
      "common": {
        "showSync": false,
        "showUpload": false,
        "showOptimize": true,
        "showAiOptimization": false,
        "showWarehouseSelection": true,
        "maximumFractionDigits": 0,
        "unservedTableInHorizontalMode": true
      },
      "unservedTable": {
        "columns": [
          {
            "title": "כתובת העמסה",
            "key": "pickup.address",
            "visible": true,
            "editable": false,
            "width": 200,
            "sortable": true
          },
          {
            "title": "כתובת פריקה",
            "key": "delivery.address",
            "visible": true,
            "editable": false,
            "width": 200,
            "sortable": true
          },
          {
            "title": "מזהה לקוח",
            "key": "customFields.0",
            "visible": true,
            "editable": false,
            "width": 120,
            "sortable": true
          },
          {
            "title": "לקוח",
            "key": "contactsInfo.companyName",
            "visible": true,
            "editable": false,
            "width": 150,
            "sortable": true
          },
          {
            "title": "שם קו",
            "key": "customFields.1",
            "visible": true,
            "editable": false,
            "width": 120,
            "sortable": true
          },
          {
            "title": "איסוף יומי קבוע",
            "key": "customFields.2",
            "visible": true,
            "editable": false,
            "width": 120,
            "sortable": true
          },
          {
            "title": "הערות לנהג",
            "key": "customFields.9",
            "visible": true,
            "editable": false,
            "width": 150,
            "sortable": true
          },
          {
            "title": "מקור נתונים",
            "key": "customFields.13",
            "visible": true,
            "editable": false,
            "width": 120,
            "sortable": true
          },
          {
            "title": "סטטוס",
            "key": "status",
            "visible": true,
            "editable": false,
            "width": 100,
            "sortable": true
          },
          {
            "title": "weight",
            "key": "weight",
            "visible": true,
            "editable": false,
            "width": 100,
            "sortable": true
          },
          {
            "title": "time start",
            "key": "constraints.deliveryTimeWindows[0].start",
            "visible": true,
            "editable": false,
            "width": 100,
            "sortable": true,
            "transformFunction": "(value, visit) => new Date(value).toLocaleDateString()"
          },
          {
            "title": "time end",
            "key": "constraints.deliveryTimeWindows[0].end",
            "visible": true,
            "editable": false,
            "width": 100,
            "sortable": true,
            "transformFunction": "(value, visit) => new Date(value).toLocaleDateString()"
          }
        ]
      },
      "filters": {
        "presets": [
          {
            "name": "מסלולים בנוים",
            "filters": [
              {
                "name": "status",
                "value": [
                  "locked"
                ]
              },
              {
                "name": "filterIgnoredTasks",
                "value": "true"
              },
              {
                "name": "isActive",
                "value": "true"
              }
            ]
          },
          {
            "id": "30",
            "name": "סניף 30",
            "filters": [
              {
                "name": "customFields.1",
                "value": [
                  "30"
                ]
              },
              {
                "name": "status",
                "value": [
                  "planning"
                ]
              },
              {
                "name": "isActive",
                "value": "true"
              }
            ]
          },
          {
            "id": "60",
            "name": "סניף 60",
            "filters": [
              {
                "name": "customFields.1",
                "value": [
                  "60"
                ]
              },
              {
                "name": "status",
                "value": [
                  "planning"
                ]
              },
              {
                "name": "isActive",
                "value": "true"
              }
            ]
          },
          {
            "id": "70",
            "name": "סניף 70",
            "filters": [
              {
                "name": "customFields.1",
                "value": [
                  "70"
                ]
              },
              {
                "name": "status",
                "value": [
                  "planning"
                ]
              },
              {
                "name": "isActive",
                "value": "true"
              }
            ]
          },
          {
            "id": "20",
            "name": "סניף 20",
            "filters": [
              {
                "name": "customFields.1",
                "value": [
                  "20"
                ]
              },
              {
                "name": "status",
                "value": [
                  "planning"
                ]
              },
              {
                "name": "isActive",
                "value": "true"
              }
            ]
          }
        ]
      },
      "visitInfo": {
        "header": {
          "primaryField": "companyName",
          "secondaryField1": "city"
        },
        "hover": {
          "secondaryField1": "({ visit }) => visit.pickup.address ? `מ: ${visit.pickup.address}` : ''",
          "secondaryField2": "({ visit }) => visit.delivery.address ? `ל: ${visit.delivery.address}` : ''"
        },
        "icons": [
          {
            "icon": "weight",
            "field": "weight"
          },
          {
            "icon": "volume",
            "field": "volume"
          },
          {
            "icon": "worth",
            "field": "({ visit }) => visit.worth"
          }
        ]
      },
      "driverSettings": {
        "global": {
          "shouldShowSecondaryDriver": false,
          "shouldSeparateTruckAndDriver": true,
          "driverSearchableFields": [
            "id",
            "name"
          ],
          "truckSearchableFields": [
            "id"
          ]
        },
        "driverSelectItems": {
          "primaryField": "name",
          "secondaryFields": [
            "customFields.1.value",
            "customFields.2.value"
          ],
          "groupField": "customFields.1.value"
        },
        "truckSelectItems": {
          "primaryField": "plateNumber",
          "secondaryFields": [
            "customFields.0.value",
            "customFields.1.value"
          ],
          "groupField": "customFields.1.value"
        }
      },
      "erp": {
        "pullOrders": true,
        "pullDataFormat": "json",
        "pullFleet": true,
        "exportToErp": true,
        "exportFields": [
          "deliveryAddressFieldUpdating",
          "pickupAddressFieldUpdating",
          "warehouseFieldUpdating"
        ],
        "actionUpdateSuffix": "..",
        "routeExport": {
          "type": "custom",
          "grouppingFunc": "(key, exportEntry, allEntries) => { const keySplit = key.split('-'); return `${keySplit[0]}-${keySplit[1]}`}",
          "sorting": {
            "groupsOrderFunc": "(keyA, keyB) => keyA < keyB? 1:0",
            "internalGroupOrderFunc": ""
          }
        }
      },
      "algo": {
        "exactTimesEnabled": true,
        "routeCapacitySettings": {
          "volumePercentage": 0.95,
          "weightPercentage": 0.95,
          "shiftDurationPercentage": 0.8,
          "shiftDurationThresholdInMinutes": 720
        },
        "customStories": {
          "processes": [],
          "stories": []
        },
        "shortDistance": {
          "estimationActive": true,
          "estimationAvarageSpeed": 50,
          "estimationUpperLimit": 30000,
          "VRPActive": true,
          "shortDistanceEarthCalculatorDistanceFactor": 0.01
        }
      },
      "fleet": {
        "fleetLoaderEnabled": true,
        "truckMaxVolume": 800,
        "truckMaxWeight": 13000,
        "defaultFleetData": {
          "defaultTruckSegment": "-",
          "defaultDriverSegment": "-",
          "truckToDriverSegmentMapping": {
            "משאית 60": [
              "נהג 60"
            ],
            "משאית 30": [
              "נהג 30"
            ],
            "משאית 20": [
              "נהג 20"
            ],
            "משאית 70": [
              "נהג 70"
            ]
          },
          "truck-segments": {
            "משאית 30": {
              "priority": 0,
              "maxWeight": 800,
              "maxVolume": 13500,
              "cost": {
                "dailyFixed": 1000,
                "perMinute": 100,
                "perKilometer": 100,
                "perStop": 0
              },
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "30",
                  "target": "Task"
                }
              ]
            },
            "משאית 60": {
              "priority": 0,
              "maxWeight": 800,
              "maxVolume": 13500,
              "cost": {
                "dailyFixed": 1000,
                "perMinute": 100,
                "perKilometer": 100,
                "perStop": 0
              },
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "60",
                  "target": "Task"
                }
              ]
            },
            "משאית 20": {
              "priority": 0,
              "maxWeight": 800,
              "maxVolume": 13500,
              "cost": {
                "dailyFixed": 1000,
                "perMinute": 100,
                "perKilometer": 100,
                "perStop": 0
              },
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "20",
                  "target": "Task"
                }
              ]
            },
            "משאית 70": {
              "priority": 0,
              "maxWeight": 800,
              "maxVolume": 13500,
              "cost": {
                "dailyFixed": 1000,
                "perMinute": 100,
                "perKilometer": 100,
                "perStop": 0
              },
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "70",
                  "target": "Task"
                }
              ]
            }
          },
          "driver-segments": {
            "נהג 30": {
              "phone": "-",
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "30",
                  "target": "Task"
                }
              ],
              "labels": [
                "DPT30"
              ],
              "shifts": [
                {
                  "start": {
                    "time": 5,
                    "location": {
                      "coordinate": {
                        "latitude": 32.042025,
                        "longitude": 34.910221
                      },
                      "address": "בארות יצחק",
                      "rawAddress": "בארות יצחק",
                      "formattedAddress": "בארות יצחק, ישראל",
                      "latitude": 32.042025,
                      "longitude": 34.910221,
                      "confidenceAlgoVersion": "2",
                      "confidence": 0.7
                    },
                    "address": "בארות יצחק"
                  },
                  "end": {
                    "time": 16,
                    "address": ""
                  }
                }
              ]
            },
            "נהג 60": {
              "phone": "-",
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "60",
                  "target": "Task"
                }
              ],
              "labels": [
                "DPT60"
              ],
              "shifts": [
                {
                  "start": {
                    "time": 5,
                    "location": {
                      "coordinate": {
                        "latitude": 32.76037,
                        "longitude": 35.31783
                      },
                      "address": "ציפורית",
                      "rawAddress": "ציפורית",
                      "formattedAddress": "ציפורית",
                      "latitude": 32.76037,
                      "longitude": 35.31783,
                      "confidenceAlgoVersion": "2",
                      "confidence": 0.7
                    },
                    "address": "ציפורית"
                  },
                  "end": {
                    "time": 16,
                    "address": ""
                  }
                }
              ]
            },
            "נהג 20": {
              "phone": "-",
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "20",
                  "target": "Task"
                }
              ],
              "labels": [
                "DPT20"
              ],
              "shifts": [
                {
                  "start": {
                    "time": 5,
                    "location": {
                      "coordinate": {
                        "latitude": 31.7623,
                        "longitude": 34.97867
                      },
                      "address": "צרעה",
                      "rawAddress": "צרעה",
                      "formattedAddress": "צרעה",
                      "latitude": 31.7623,
                      "longitude": 34.97867,
                      "confidenceAlgoVersion": "2",
                      "confidence": 0.7
                    },
                    "address": "צרעה"
                  },
                  "end": {
                    "time": 16,
                    "address": ""
                  }
                }
              ]
            },
            "נהג 70": {
              "phone": "-",
              "customFields": [
                {
                  "id": "customFields.1",
                  "value": "70",
                  "target": "Task"
                }
              ],
              "labels": [
                "DPT70"
              ],
              "shifts": [
                {
                  "start": {
                    "time": 5,
                    "location": {
                      "coordinate": {
                        "latitude": 31.22249,
                        "longitude": 34.80152
                      },
                      "address": "באר שבע",
                      "rawAddress": "באר שבע",
                      "formattedAddress": "באר שבע",
                      "latitude": 31.22249,
                      "longitude": 34.80152,
                      "confidenceAlgoVersion": "2",
                      "confidence": 0.7
                    },
                    "address": "באר שבע"
                  },
                  "end": {
                    "time": 16,
                    "address": ""
                  }
                }
              ]
            }
          }
        },
        "automaticFleetSync": false,
        "activateSyncOnFleetPickup": false,
        "spaceMangerEnabled": false,
        "pickupShiftEndTime": 194400000
      },
      "visit": {
        "itemsLockEnabled": false,
        "haveWorth": true,
        "taskEditorInvalidLocationConfidenceRange": [
          0,
          0.99
        ],
        "visitCanServeLocationConfidenceRange": [
          0.1,
          1
        ],
        "visitLocationRedMarksConfidenceRange": [
          0,
          0.2
        ],
        "visitLocationYellowMarkConfidenceRange": [
          0.3,
          0.99
        ]
      },
      "map": {
        "maxUnservedPoints": 1500,
        "mapClusterMaxZoom": 10,
        "contextMenuOptions": {
          "ignoreInPlan": {
            "enabled": false,
            "textColor": "red"
          },
          "removeFromRoute": {
            "enabled": false
          },
          "enableMapMarkersSpreading": false
        }
      },
      "topBarActions": {
        "sync": [
          "erp-sync"
        ],
        "optimize": [
          "vrp",
          "knapsack"
        ]
      }
    },
    "accounts": {
      "appId": "accounts"
    },
    "dataExplorer": {
      "appId": "dataExplorer",
      "dataSources": [
        {
          "id": 1,
          "name": "task items",
          "displayName": "Items",
          "aggregation": [
            {
              "columnName": "amount",
              "groupByColumns": [
                "sku"
              ],
              "func": "(columnId, leafRows, childRows) => {\n  const sumAll = childRows.reduce(\n    (prev, row) => prev + parseFloat(row?.original[columnId] ?? 0),\n    0\n  );\n  const sumActive = childRows\n    .filter((c) => c?.original[\"isActive\"] === 'לתכנון')\n    .reduce((prev, row) => prev + parseFloat(row?.original[columnId] ?? 0), 0) ?? 0;\n  const inStock = parseFloat(childRows[0].original[\"customFields1\"]) ?? 0;\n\n  let result = \"\";\n\n  if (!isNaN(Number(value?.inStock))) return \"0\";\n\n  if (sumActive <= inStock) {\n    result = { value: `${sumActive} מתוך ${inStock} במלאי`, color: \"\" }\n  }\n  if (sumActive > inStock) {\n  result = { value: `${sumActive} מתוך ${inStock} במלאי`, color: \"red\" }\n  }\n  if (sumActive !== sumAll && sumAll <= inStock) {\n  result = {\n      value: `${sumActive} מתוך ${inStock} במלאי`,\n      color: \"blue\",\n    }\n  }\n\n  return result;\n}",
              "displayFunction": "(value) => value;"
            },
            {
              "columnName": "customFields0",
              "groupByColumns": [
                "routeNumber"
              ],
              "func": "sum",
              "displayFunction": "(value)=> parseFloat( value?.toLocaleString(undefined, { maximumFractionDigits: 2}) ) ?? ''"
            },
            {
              "columnName": "eta",
              "groupByColumns": [
                "routeNumber"
              ],
              "func": "(columnId, leafRows, childRows) => childRows?.[0].original['route']?.time",
              "displayFunction": "(value) =>  value??''"
            },
            {
              "columnName": "deliveryAddress",
              "groupByColumns": [
                "routeNumber"
              ],
              "func": "(columnId, leafRows, childRows) => childRows?.[0].original['route']?.distance ?? '' ",
              "displayFunction": "(value) =>  value??'' "
            },
            {
              "columnName": "volume",
              "groupByColumns": [
                "routeNumber",
                "orderId"
              ],
              "func": "(columnId, leafRows, childRows) =>  `${childRows.reduce((prev, row) => prev + parseFloat(row?.original[columnId] ?? 0) , 0).toLocaleString(undefined, { maximumFractionDigits: 2})  }/${childRows[0].original['truck']?.maxVolume?? 0}`",
              "displayFunction": "(value) => value?.endsWith('/') ? '': value "
            },
            {
              "columnName": "weight",
              "groupByColumns": [
                "routeNumber",
                "orderId"
              ],
              "func": "(columnId, leafRows, childRows) =>  `${childRows.reduce((prev, row) => prev + parseFloat(row?.original[columnId] ?? 0) , 0).toLocaleString(undefined, { maximumFractionDigits: 2}) }/${childRows[0].original['truck']?.maxWeight?? 0}`",
              "displayFunction": "(value) => value?.endsWith('/') ? '': value "
            }
          ],
          "views": [
            {
              "id": 3,
              "displayName": "כללי",
              "sortBy": [
                {
                  "id": "customer",
                  "desc": true
                }
              ],
              "groupBy": [],
              "columnOrder": [
                {
                  "name": "routeStatus",
                  "index": 0
                },
                {
                  "name": "customer",
                  "index:": 0
                },
                {
                  "name": "sku",
                  "index:": 1
                },
                {
                  "name": "description",
                  "index:": 2
                },
                {
                  "name": "priority",
                  "index:": 2
                },
                {
                  "name": "customFields0",
                  "index:": 3
                },
                {
                  "name": "amount",
                  "index:": 4
                },
                {
                  "name": "deliveryAddress",
                  "index:": 6
                },
                {
                  "name": "comment",
                  "index:": 7
                },
                {
                  "name": "routeNumber",
                  "index:": 8
                },
                {
                  "name": "driverName",
                  "index:": 9
                },
                {
                  "name": "visitType",
                  "index:": 10
                },
                {
                  "name": "orderId",
                  "index:": 11
                },
                {
                  "name": "tags",
                  "index:": 12
                },
                {
                  "name": "dueDate",
                  "index:": 13
                },
                {
                  "name": "lineId",
                  "index:": 14
                },
                {
                  "name": "volume",
                  "index:": 15
                },
                {
                  "name": "weight",
                  "index:": 16
                },
                {
                  "name": "pickupAddress",
                  "index:": 17
                },
                {
                  "name": "eta",
                  "index:": 18
                },
                {
                  "name": "pickupTimeWindows",
                  "index:": 19
                },
                {
                  "name": "deliveryTimeWindows",
                  "index:": 20
                },
                {
                  "name": "packageId",
                  "index:": 21
                },
                {
                  "name": "customFields1",
                  "index:": 22
                },
                {
                  "name": "customFields2",
                  "index:": 23
                }
              ],
              "columnVisibility": {},
              "filterBy": [
                {
                  "id": 1,
                  "filterType": "column",
                  "columnName": "sku",
                  "filterName": "sku"
                },
                {
                  "id": 2,
                  "filterType": "column",
                  "columnName": "description",
                  "filterName": "description"
                },
                {
                  "id": 3,
                  "filterType": "column",
                  "columnName": "customFields0",
                  "filterName": "customFields0"
                },
                {
                  "id": 4,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountLowerThanEqual"
                },
                {
                  "id": 5,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountGreaterThanEqual"
                },
                {
                  "id": 6,
                  "filterType": "column",
                  "columnName": "customer",
                  "filterName": "customer"
                },
                {
                  "id": 7,
                  "filterType": "column",
                  "columnName": "driverName",
                  "filterName": "driverName"
                },
                {
                  "id": 8,
                  "filterType": "column",
                  "columnName": "deliveryAddress",
                  "filterName": "deliveryAddress"
                },
                {
                  "id": 9,
                  "filterType": "column",
                  "columnName": "routeNumber",
                  "filterName": "routeNumber"
                },
                {
                  "id": 10,
                  "filterType": "column",
                  "columnName": "customFields2",
                  "filterName": "customFields2"
                },
                {
                  "id": 11,
                  "filterType": "column",
                  "columnName": "tags",
                  "filterName": "tags"
                },
                {
                  "id": 12,
                  "filterType": "column",
                  "columnName": "dueDate",
                  "filterName": "dueDate"
                },
                {
                  "id": 13,
                  "filterType": "column",
                  "columnName": "priority",
                  "filterName": "priority"
                },
                {
                  "id": 14,
                  "filterType": "column",
                  "columnName": "isActive",
                  "filterName": "isActiveEqual"
                }
              ],
              "style": {
                "row1": {
                  "color": "(row) => row['isActive'] === 'לא לתכנון' ? '#AAAFB4' : '' ",
                  "backgroundColor": "(row) => row['isActive'] === 'לא לתכנון' && row['customFields14'] === 'לתכנון' ? '##0080FF' : ''"
                }
              }
            },
            {
              "id": 1,
              "displayName": "בדיקת מלאי",
              "sortBy": [
                {
                  "id": "amount",
                  "desc": true
                }
              ],
              "groupBy": [
                "sku"
              ],
              "columnOrder": [
                {
                  "name": "sku",
                  "index:": 0
                },
                {
                  "name": "description",
                  "index:": 1
                },
                {
                  "name": "customFields0",
                  "index:": 2
                },
                {
                  "name": "amount",
                  "index:": 3
                },
                {
                  "name": "isActive",
                  "index:": 3
                },
                {
                  "name": "customer",
                  "index:": 4
                },
                {
                  "name": "deliveryAddress",
                  "index:": 5
                },
                {
                  "name": "comment",
                  "index:": 6
                },
                {
                  "name": "orderId",
                  "index:": 6
                },
                {
                  "name": "lineId",
                  "index:": 7
                },
                {
                  "name": " customFields2",
                  "index:": 8
                },
                {
                  "name": "routeNumber",
                  "index:": 9
                },
                {
                  "name": "driverName",
                  "index:": 10
                },
                {
                  "name": "deliveryTimeWindows",
                  "index:": 11
                },
                {
                  "name": "customFields2",
                  "index:": 12
                },
                {
                  "name": "tags",
                  "index:": 10
                },
                {
                  "name": "dueDate",
                  "index:": 11
                },
                {
                  "name": "priority",
                  "index:": 4
                }
              ],
              "columnVisibility": {
                "visitType": false,
                "volume": false,
                "weight": false,
                "pickupAddress": false,
                "eta": false,
                "pickupTimeWindows": false,
                "packageId": false,
                "customFields1": false,
                "deliveryTimeWindows": false,
                "orderLineId": false,
                "routeNumber": false,
                "lineId": false,
                "driverName": false,
                "isActive": true
              },
              "filterBy": [
                {
                  "id": 1,
                  "filterType": "column",
                  "columnName": "sku",
                  "filterName": "sku"
                },
                {
                  "id": 2,
                  "filterType": "column",
                  "columnName": "description",
                  "filterName": "description"
                },
                {
                  "id": 3,
                  "filterType": "column",
                  "columnName": "customFields0",
                  "filterName": "customFields0"
                },
                {
                  "id": 4,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountLowerThanEqual"
                },
                {
                  "id": 5,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountGreaterThanEqual",
                  "values": [
                    "1"
                  ]
                },
                {
                  "id": 6,
                  "filterType": "column",
                  "columnName": "customer",
                  "filterName": "customer"
                },
                {
                  "id": 7,
                  "filterType": "column",
                  "columnName": "driverName",
                  "filterName": "driverName"
                },
                {
                  "id": 8,
                  "filterType": "column",
                  "columnName": "deliveryAddress",
                  "filterName": "deliveryAddress"
                },
                {
                  "id": 9,
                  "filterType": "column",
                  "columnName": "customFields2",
                  "filterName": "customFields2"
                },
                {
                  "id": 10,
                  "filterType": "column",
                  "columnName": "tags",
                  "filterName": "tags",
                  "values": [
                    "'לא פרויקט'"
                  ]
                },
                {
                  "id": 12,
                  "filterType": "column",
                  "columnName": "dueDate",
                  "filterName": "dueDate"
                },
                {
                  "id": 13,
                  "filterType": "column",
                  "columnName": "priority",
                  "filterName": "priority"
                },
                {
                  "id": 14,
                  "filterType": "column",
                  "columnName": "isActive",
                  "filterName": "isActiveEqual"
                }
              ],
              "style": {
                "row1": {
                  "color": "(row) => row['isActive'] === 'לא לתכנון' ? '#AAAFB4' : '' ",
                  "backgroundColor": "(row) => row['isActive'] === 'לא לתכנון' && row['customFields14'] === 'לתכנון' ? '##0080FF' : ''"
                }
              }
            },
            {
              "id": 2,
              "displayName": "תוכן משאית",
              "columnOrder": [
                {
                  "name": "routeNumber",
                  "index:": 0
                },
                {
                  "name": "driverName",
                  "index:": 1
                },
                {
                  "name": "customer",
                  "index:": 2
                },
                {
                  "name": "deliveryAddress",
                  "index:": 3
                },
                {
                  "name": "comment",
                  "index:": 4
                },
                {
                  "name": "visitType",
                  "index:": 5
                },
                {
                  "name": "orderId",
                  "index:": 6
                },
                {
                  "name": "sku",
                  "index:": 7
                },
                {
                  "name": "description",
                  "index:": 8
                },
                {
                  "name": "amount",
                  "index:": 9
                },
                {
                  "name": "volume",
                  "index:": 10
                },
                {
                  "name": "weight",
                  "index:": 0
                },
                {
                  "name": "deliveryTimeWindows",
                  "index:": 0
                },
                {
                  "name": "tags",
                  "index:": 10
                },
                {
                  "name": "dueDate",
                  "index:": 11
                },
                {
                  "name": "priority",
                  "index:": 4
                }
              ],
              "columnVisibility": {
                "customFields0": false,
                "pickupAddress": false,
                "pickupTimeWindows": false,
                "deliveryTimeWindows": false,
                "packageId": false,
                "customFields1": false,
                "customFields2": false
              },
              "sortBy": [
                {
                  "id": "amount",
                  "desc": true
                }
              ],
              "groupBy": [
                "routeNumber"
              ],
              "filterBy": [
                {
                  "id": 1,
                  "filterType": "column",
                  "columnName": "routeNumber",
                  "filterName": "routeNumber"
                },
                {
                  "id": 2,
                  "filterType": "column",
                  "columnName": "driverName",
                  "filterName": "driverName"
                },
                {
                  "id": 3,
                  "filterType": "column",
                  "columnName": "customer",
                  "filterName": "customer"
                },
                {
                  "id": 4,
                  "filterType": "column",
                  "columnName": "deliveryAddress",
                  "filterName": "deliveryAddress"
                },
                {
                  "id": 5,
                  "filterType": "column",
                  "columnName": "visitType",
                  "filterName": "visitType"
                },
                {
                  "id": 6,
                  "filterType": "column",
                  "columnName": "deliveryAddress",
                  "filterName": "deliveryAddress"
                },
                {
                  "id": 7,
                  "filterType": "column",
                  "columnName": "sku",
                  "filterName": "sku"
                },
                {
                  "id": 8,
                  "filterType": "column",
                  "columnName": "description",
                  "filterName": "description"
                },
                {
                  "id": 9,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountLowerThanEqual"
                },
                {
                  "id": 10,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountGreaterThanEqual"
                },
                {
                  "id": 11,
                  "filterType": "column",
                  "columnName": "volume",
                  "filterName": "volume"
                },
                {
                  "id": 12,
                  "filterType": "column",
                  "columnName": "weight",
                  "filterName": "weight"
                },
                {
                  "id": 13,
                  "filterType": "column",
                  "columnName": "tags",
                  "filterName": "tags"
                },
                {
                  "id": 14,
                  "filterType": "column",
                  "columnName": "dueDate",
                  "filterName": "dueDate"
                },
                {
                  "id": 15,
                  "filterType": "column",
                  "columnName": "priority",
                  "filterName": "priority"
                },
                {
                  "id": 16,
                  "filterType": "column",
                  "columnName": "isActive",
                  "filterName": "isActiveEqual"
                }
              ],
              "style": {
                "row1": {
                  "color": "(row) => row['isActive'] === 'לא לתכנון' ? '#AAAFB4' : '' ",
                  "backgroundColor": "(row) => row['isActive'] === 'לא לתכנון' && row['customFields14'] === 'לתכנון' ? '##0080FF' : ''"
                }
              }
            },
            {
              "id": 4,
              "displayName": "הזמנות",
              "sortBy": [
                {
                  "id": "customer",
                  "desc": false
                }
              ],
              "groupBy": [
                "orderId"
              ],
              "columnOrder": [
                {
                  "name": "customer",
                  "index:": 0
                },
                {
                  "name": "sku",
                  "index:": 1
                },
                {
                  "name": "description",
                  "index:": 2
                },
                {
                  "name": "customFields0",
                  "index:": 3
                },
                {
                  "name": "amount",
                  "index:": 4
                },
                {
                  "name": "deliveryAddress",
                  "index:": 6
                },
                {
                  "name": "comment",
                  "index:": 7
                },
                {
                  "name": "routeNumber",
                  "index:": 8
                },
                {
                  "name": "driverName",
                  "index:": 9
                },
                {
                  "name": "visitType",
                  "index:": 10
                },
                {
                  "name": "orderId",
                  "index:": 11
                },
                {
                  "name": "tags",
                  "index:": 12
                },
                {
                  "name": "dueDate",
                  "index:": 13
                },
                {
                  "name": "lineId",
                  "index:": 14
                },
                {
                  "name": "volume",
                  "index:": 15
                },
                {
                  "name": "weight",
                  "index:": 16
                },
                {
                  "name": "pickupAddress",
                  "index:": 17
                },
                {
                  "name": "eta",
                  "index:": 18
                },
                {
                  "name": "pickupTimeWindows",
                  "index:": 19
                },
                {
                  "name": "deliveryTimeWindows",
                  "index:": 20
                },
                {
                  "name": "packageId",
                  "index:": 21
                },
                {
                  "name": "customFields1",
                  "index:": 22
                },
                {
                  "name": "customFields2",
                  "index:": 23
                },
                {
                  "name": "priority",
                  "index:": 4
                }
              ],
              "columnVisibility": {},
              "filterBy": [
                {
                  "id": 1,
                  "filterType": "column",
                  "columnName": "sku",
                  "filterName": "sku"
                },
                {
                  "id": 2,
                  "filterType": "column",
                  "columnName": "description",
                  "filterName": "description"
                },
                {
                  "id": 3,
                  "filterType": "column",
                  "columnName": "customFields0",
                  "filterName": "customFields0"
                },
                {
                  "id": 4,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountLowerThanEqual"
                },
                {
                  "id": 5,
                  "filterType": "column",
                  "columnName": "amount",
                  "filterName": "amountGreaterThanEqual"
                },
                {
                  "id": 6,
                  "filterType": "column",
                  "columnName": "customer",
                  "filterName": "customer"
                },
                {
                  "id": 7,
                  "filterType": "column",
                  "columnName": "driverName",
                  "filterName": "driverName"
                },
                {
                  "id": 8,
                  "filterType": "column",
                  "columnName": "deliveryAddress",
                  "filterName": "deliveryAddress"
                },
                {
                  "id": 9,
                  "filterType": "column",
                  "columnName": "routeNumber",
                  "filterName": "routeNumber"
                },
                {
                  "id": 10,
                  "filterType": "column",
                  "columnName": "customFields2",
                  "filterName": "customFields2"
                },
                {
                  "id": 11,
                  "filterType": "column",
                  "columnName": "tags",
                  "filterName": "tags"
                },
                {
                  "id": 12,
                  "filterType": "column",
                  "columnName": "dueDate",
                  "filterName": "dueDate"
                },
                {
                  "id": 13,
                  "filterType": "column",
                  "columnName": "priority",
                  "filterName": "priority"
                },
                {
                  "id": 14,
                  "filterType": "column",
                  "columnName": "isActive",
                  "filterName": "isActiveEqual"
                }
              ],
              "style": {
                "row1": {
                  "color": "(row) => row['isActive'] === 'לא לתכנון' ? '#AAAFB4' : '' ",
                  "backgroundColor": "(row) => row['isActive'] === 'לא לתכנון' && row['customFields14'] === 'לתכנון' ? '##0080FF' : ''"
                }
              }
            }
          ],
          "filters": [
            {
              "id": 1,
              "name": "routeNumber",
              "displayName": "מסלול",
              "dataType": "dropDown",
              "functionNames": [
                "equal"
              ],
              "multipleItems": true,
              "values": "(rows)=> rows.map((row) => row['routeNumber'])"
            },
            {
              "id": 2,
              "name": "weight",
              "displayName": "משקל",
              "dataType": "float",
              "functionNames": [
                "equal"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 3,
              "name": "dueDate",
              "displayName": "תאריך אספקה",
              "dataType": "date",
              "functionNames": [
                "date"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 4,
              "name": "orderId",
              "displayName": "הזמנה",
              "dataType": "dropDown",
              "functionNames": [
                "contain"
              ],
              "multipleItems": true,
              "values": "(rows)=> rows.map((row) => row['orderId'])"
            },
            {
              "id": 5,
              "name": "driverName",
              "displayName": "נהג",
              "dataType": "dropDown",
              "functionNames": [
                "contain"
              ],
              "multipleItems": true,
              "values": "(rows)=> rows.map((row) => row['driverName'])"
            },
            {
              "id": 6,
              "name": "volume",
              "displayName": "נפח",
              "dataType": "float",
              "functionNames": [
                "equal"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 7,
              "name": "tags",
              "displayName": "תגיות",
              "dataType": "multiselect",
              "functionNames": [
                "contain"
              ],
              "multipleItems": true,
              "values": "(rows)=> {const tags = new Set(rows.map((row) => row['tags'].split(', ')).flat()); return [...tags]}"
            },
            {
              "id": 8,
              "name": "sku",
              "displayName": "מק״ט",
              "dataType": "text",
              "functionNames": [
                "contain"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 9,
              "name": "description",
              "displayName": "תיאור",
              "dataType": "text",
              "functionNames": [
                "contain"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 10,
              "name": "customFields0",
              "displayName": "כמות בהזמנה",
              "dataType": "int",
              "functionNames": [
                "equal"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 11,
              "name": "amountGreaterThanEqual",
              "displayName": "כמות גדולה מ",
              "dataType": "float",
              "functionNames": [
                "greaterThanEqual"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 12,
              "name": "deliveryAddress",
              "displayName": "כתובת פריקה...",
              "dataType": "text",
              "functionNames": [
                "contain"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 13,
              "name": "customer",
              "displayName": "שם לקוח",
              "dataType": "text",
              "functionNames": [
                "contain"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 14,
              "name": "customFields2",
              "displayName": "תאריך לתכנון",
              "dataType": "date",
              "functionNames": [
                "date"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 15,
              "name": "priority",
              "displayName": "עדיפות",
              "dataType": "multiselect",
              "functionNames": [
                "equal"
              ],
              "multipleItems": true,
              "values": [
                "גבוהה",
                "נמוכה",
                "בינונית"
              ]
            },
            {
              "id": 16,
              "name": "amountLowerThanEqual",
              "displayName": "כמות קטנה מ",
              "dataType": "float",
              "functionNames": [
                "lowerThanEqual"
              ],
              "multipleItems": true,
              "values": []
            },
            {
              "id": 17,
              "name": "isActiveEqual",
              "displayName": "לתכנון",
              "dataType": "dropDown",
              "functionNames": [
                "equal"
              ],
              "multipleItems": true,
              "values": [
                "לתכנון",
                "לא לתכנון"
              ]
            }
          ],
          "columns": [
            {
              "name": "sku",
              "displayName": "מק״ט",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "groupable": true,
              "columnWidth": 150,
              "filterable": true,
              "accessKey": "sku",
              "transformFunction": "(value)=> value || 'NO SKU'",
              "toSourceValueFunction": "(value)=> value.replace('NO SKU', '')",
              "values": []
            },
            {
              "name": "description",
              "displayName": "תיאור",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "columnWidth": 400,
              "sortable": true,
              "groupable": false,
              "filterable": true,
              "accessKey": "description",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "customFields0",
              "displayName": "כ.בהזמנה",
              "dataType": "int",
              "visible": true,
              "editable": true,
              "sortable": true,
              "groupable": true,
              "columnWidth": 140,
              "filterable": true,
              "accessKey": "customFields0",
              "transformFunction": "(value)=> Number(value) ?? 0 ",
              "values": []
            },
            {
              "name": "amount",
              "displayName": "כמות",
              "dataType": "float",
              "visible": true,
              "editable": true,
              "columnWidth": 180,
              "sortable": true,
              "groupable": false,
              "filterable": true,
              "accessKey": "amount",
              "transformFunction": "(value) => parseFloat( value?.toLocaleString(undefined, { maximumFractionDigits: 2 }) ) ?? '';",
              "toSourceValueFunction": "(value) => parseFloat(value) ?? 0",
              "values": []
            },
            {
              "name": "customer",
              "displayName": "שם לקוח",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "columnWidth": 350,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "accessKey": "customer",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "deliveryAddress",
              "displayName": "כתובת פריקה...",
              "dataType": "text",
              "visible": true,
              "columnWidth": 200,
              "editable": false,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "accessKey": "deliveryAddress",
              "transformFunction": "(value)=> value",
              "values": []
            },
            {
              "name": "comment",
              "displayName": "הערות",
              "dataType": "text",
              "visible": true,
              "columnWidth": 250,
              "editable": true,
              "sortable": false,
              "groupable": false,
              "filterable": false,
              "groupByFunction": "",
              "accessKey": "comment",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "routeNumber",
              "displayName": "מסלול",
              "dataType": "dropDown",
              "visible": true,
              "editable": true,
              "sortable": true,
              "columnWidth": 130,
              "groupable": true,
              "filterable": true,
              "accessKey": "routeNumber",
              "transformFunction": "(value)=> value && !isNaN(Number(value)) ? (Number(value) + 1) :'לא במסלול'",
              "toSourceValueFunction": "(value)=> value.replace('לא במסלול', -1)",
              "values": "(rows, mgr)=> { const routeNumber = mgr?.routeNumbers?.map((num) => num.toString()); const results = ['לא במסלול']; if (routeNumber?.length) results.push(...routeNumber); return results; }"
            },
            {
              "name": "driverName",
              "displayName": "שם הנהג",
              "dataType": "dropDown",
              "visible": true,
              "editable": false,
              "sortable": true,
              "groupable": true,
              "columnWidth": 200,
              "filterable": true,
              "accessKey": "driverName",
              "transformFunction": "",
              "values": []
            },
            {
              "accessKey": "visitType",
              "name": "visitType",
              "displayName": "סוג ביקור",
              "dataType": "dropDown",
              "visible": true,
              "editable": true,
              "sortable": true,
              "columnWidth": 130,
              "groupable": true,
              "filterable": true,
              "aggregationFn": "",
              "toSourceValueFunction": "(value , manager)=> manager.visitTypeOptions.find((v) => v.text  ==  value)?.value || value",
              "transformFunction": "(value , manager) => { return manager.visitTypeOptions.find((v) => v.value  ==  value)?.text || value }",
              "values": "(rows , manager) => manager.visitTypeOptions ?? []"
            },
            {
              "name": "priority",
              "displayName": "עדיפות",
              "dataType": "dropDown",
              "visible": true,
              "editable": true,
              "sortable": true,
              "groupable": true,
              "columnWidth": 150,
              "filterable": true,
              "accessKey": "priority",
              "transformFunction": "(value) => { return ( [[4, 'גבוהה'] ,[2, 'בינונית'],[ 1, 'נמוכה']].find( (priority) => priority[0] === value )?.[1] ?? '' ); }",
              "toSourceValueFunction": "(value) =>  [[4, 'גבוהה'] ,[2, 'בינונית'],[ 1, 'נמוכה']].find((priority) => priority[1].includes(value) )?.[0] ?? ''",
              "values": [
                "גבוהה",
                "נמוכה",
                "בינונית"
              ]
            },
            {
              "name": "orderId",
              "displayName": "הזמנה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "accessKey": "orderId",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "tags",
              "displayName": "תגיות",
              "dataType": "dropDown",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 200,
              "groupable": true,
              "filterable": true,
              "accessKey": "tags",
              "transformFunction": "(value) => `'` + value?.join('\\', \\'') + `'` ??''",
              "values": []
            },
            {
              "accessKey": "dueDate",
              "name": "dueDate",
              "displayName": "ת.אספקה",
              "dataType": "date",
              "visible": true,
              "editable": false,
              "columnWidth": 150,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "transformFunction": "(value)=> new Date(value)?.toLocaleDateString('en-GB') ?? ''",
              "values": []
            },
            {
              "name": "lineId",
              "displayName": "שורה",
              "dataType": "int",
              "visible": true,
              "editable": false,
              "sortable": true,
              "groupable": false,
              "columnWidth": 120,
              "filterable": true,
              "accessKey": "lineId",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "volume",
              "displayName": "נפח",
              "dataType": "float",
              "visible": true,
              "editable": true,
              "sortable": true,
              "groupable": false,
              "columnWidth": 130,
              "filterable": true,
              "accessKey": "volume",
              "transformFunction": "(value) => parseFloat( value?.toLocaleString(undefined, { maximumFractionDigits: 2 }) ) ?? '';",
              "toSourceValueFunction": "(value) => parseFloat(value) ?? 0",
              "values": []
            },
            {
              "name": "weight",
              "displayName": "משקל",
              "dataType": "float",
              "visible": true,
              "editable": true,
              "sortable": true,
              "columnWidth": 130,
              "groupable": false,
              "filterable": true,
              "accessKey": "weight",
              "transformFunction": "(value) => parseFloat( value?.toLocaleString(undefined, { maximumFractionDigits: 2 }) ) ?? '';",
              "toSourceValueFunction": "(value) => parseFloat(value) ?? 0",
              "values": []
            },
            {
              "name": "pickupAddress",
              "displayName": "כתובת העמסה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "columnWidth": 200,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "accessKey": "pickupAddress",
              "transformFunction": "(value)=> value",
              "values": []
            },
            {
              "name": "eta",
              "displayName": "צפי הגעה",
              "dataType": "time",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 130,
              "groupable": true,
              "filterable": true,
              "accessKey": "eta",
              "transformFunction": "(value) => { const seconds = parseInt(value) ?? 0 % 86400; if(!seconds) return ''; var hours = Math.floor(seconds / 3600); var minutes = Math.floor((seconds % 3600) / 60); var HH = ('0' + hours).slice(-2); var mm = ('0' + minutes).slice(-2); return HH + ':' + mm; }",
              "values": []
            },
            {
              "name": "pickupTimeWindows",
              "displayName": "חלון זמן העמסה",
              "dataType": "dateAndTime",
              "visible": true,
              "editable": false,
              "sortable": true,
              "groupable": false,
              "filterable": true,
              "accessKey": "pickupTimeWindows",
              "transformFunction": " (timeWindows) => { let datStr = ''; if (!timeWindows?.[0]?.start) return null; const timeWindow = timeWindows?.[0]; if (timeWindow) { const date = new Date(timeWindow?.start).toLocaleDateString('en-GB'); const start = new Date(timeWindow?.start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit',  hour12: false }); const end = new Date(timeWindow?.end).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit',  hour12: false } ); if (date && start && end) { datStr = `${date} ${start}-${end}`; } } return datStr; }",
              "values": []
            },
            {
              "name": "deliveryTimeWindows",
              "displayName": "חלון זמן פריקה",
              "dataType": "dateAndTime",
              "visible": true,
              "editable": false,
              "sortable": true,
              "groupable": false,
              "filterable": true,
              "accessKey": "deliveryTimeWindows",
              "transformFunction": " (timeWindows) => { let datStr = ''; if (!timeWindows?.[0]?.start) return null; const timeWindow = timeWindows?.[0]; if (timeWindow) { const date = new Date(timeWindow?.start).toLocaleDateString('en-GB'); const start = new Date(timeWindow?.start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit',  hour12: false }); const end = new Date(timeWindow?.end).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit',  hour12: false } ); if (date && start && end) { datStr = `${date} ${start}-${end}`; } } return datStr; }",
              "values": []
            },
            {
              "name": "packageId",
              "displayName": "קיט",
              "dataType": "dropDown",
              "visible": true,
              "editable": true,
              "sortable": true,
              "groupable": true,
              "columnWidth": 130,
              "filterable": true,
              "accessKey": "packageId",
              "transformFunction": "",
              "values": "(rows) => rows.map((row) => row?.packageId)"
            },
            {
              "name": "customFields1",
              "displayName": "כ.במלאי",
              "dataType": "int",
              "visible": true,
              "editable": true,
              "sortable": true,
              "columnWidth": 135,
              "groupable": true,
              "filterable": true,
              "accessKey": "customFields1",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "customFields2",
              "displayName": "תאריך לתכנון",
              "dataType": "date",
              "visible": true,
              "editable": true,
              "columnWidth": 130,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "accessKey": "customFields2",
              "transformFunction": "(value)=> value?.replaceAll('.', '/')??''",
              "values": []
            },
            {
              "name": "routeStatus",
              "displayName": "סטטוס מסלול",
              "dataType": "dropDown",
              "visible": true,
              "editable": false,
              "columnWidth": 130,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "accessKey": "routeStatus",
              "transformFunction": " (value) => { if (value === 'planning') { return 'לא נעול'; } else if (value === 'locked') { return 'נעול'; } else { return ''; } }",
              "values": []
            },
            {
              "name": "isActive",
              "displayName": "לתכנון",
              "dataType": "text",
              "visible": true,
              "editable": true,
              "columnWidth": 130,
              "sortable": true,
              "groupable": true,
              "filterable": true,
              "accessKey": "isActive",
              "transformFunction": "(value) => { return ( [[true, 'לתכנון'] ,[false, 'לא לתכנון']].find( (isActive) => isActive[0] === value )?.[1] ?? '' ); }",
              "toSourceValueFunction": "(value) => value",
              "values": [
                "לתכנון",
                "לא לתכנון"
              ]
            }
          ],
          "query": {
            "request": {
              "url": "",
              "method": "GET/POST",
              "body": {},
              "headers": {
                "": ""
              }
            },
            "existing": {
              "getDataFunction": "()=> planMgrService.getPlanData()",
              "func": "(data)=> dataExplorerTransformationService.transformPlanDataToItems(data)",
              "flatFormula": "",
              "parameters": []
            }
          },
          "export": {
            "function": "(target, field, rowsSearchPartials, value) => planMgrService.setPLanItem(target, field, rowsSearchPartials, value)",
            "columns": [
              {
                "id": 1,
                "columnName": "weight",
                "target": "visits.items"
              },
              {
                "id": 2,
                "columnName": "volume",
                "target": "visits.items"
              },
              {
                "id": 3,
                "columnName": "amount",
                "target": "visits.items"
              },
              {
                "id": 4,
                "columnName": "comment",
                "target": "visits.items"
              },
              {
                "id": 5,
                "columnName": "packageId",
                "target": "visits.items"
              },
              {
                "id": 6,
                "columnName": "customFields0",
                "target": "visits.items"
              },
              {
                "id": 7,
                "columnName": "customFields1",
                "target": "visits.items"
              },
              {
                "id": 8,
                "columnName": "priority",
                "target": "visits.items"
              },
              {
                "id": 9,
                "columnName": "routeNumber",
                "target": "visits"
              },
              {
                "id": 10,
                "columnName": "isActive",
                "target": "visits.items"
              }
            ],
            "fieldsMap": [
              {
                "target": "visits.items",
                "searchKeys": [
                  "itemId"
                ],
                "options": {
                  "itemId": "id",
                  "customFields0": "customFields.0",
                  "customFields1": "customFields.1",
                  "customFields2": "customFields.2",
                  "isActive": "isActive"
                }
              },
              {
                "target": "visits",
                "searchKeys": [
                  "visitId"
                ],
                "options": {
                  "visitId": "id"
                }
              },
              {
                "target": "trucks",
                "searchKeys": [
                  "trucksId"
                ],
                "options": {}
              },
              {
                "target": "routes",
                "searchKeys": [
                  "routeId"
                ],
                "options": {
                  "routeId": "id"
                }
              }
            ]
          },
          "actions": [
            {
              "columnName": "routeNumber",
              "matchedColumns": [
                "visitId"
              ],
              "onAction": "edit",
              "function": "setFieldWithSameValue"
            }
          ],
          "summary": {
            "func": "(selectedRows)=>[]"
          },
          "footerActions": {
            "allowPlanStateChange": true
          }
        },
        {
          "id": 2,
          "name": "fleet",
          "displayName": "צי",
          "aggregation": [],
          "views": [
            {
              "id": 1,
              "displayName": "מסלולים",
              "sortBy": [],
              "groupBy": [],
              "columnOrder": [],
              "columnVisibility": {},
              "filterBy": []
            }
          ],
          "filters": [],
          "columns": [
            {
              "name": "routeNumber",
              "displayName": "מספר מסלול",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "routeNumber",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "drivers",
              "displayName": "נהגים",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "drivers",
              "transformFunction": "(value) =>Array.from(new Set(value))?.map((driver) => driver.name).join(', ')",
              "values": []
            },
            {
              "name": "truckTags",
              "displayName": "תגיות נהג",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "truckTags",
              "transformFunction": "(value) => value?.join(', ')",
              "values": []
            },
            {
              "name": "platNumber",
              "displayName": "משאיות",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "platNumber",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "truckTags",
              "displayName": "תגיות משאית",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "truckTags",
              "transformFunction": "(value) => value?.join(', ')",
              "values": []
            },
            {
              "name": "startAddress",
              "displayName": "כתובת התחלה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "startAddress",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "endAddress",
              "displayName": "כתובת סיום",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "endAddress",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "deliveriesCount",
              "displayName": "מספר נקודות פריקה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "deliveriesCount",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "volume",
              "displayName": "סך נפח הזמנות",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "volume",
              "transformFunction": "(value)=>  parseFloat( value ? (value).toLocaleString(undefined, { maximumFractionDigits: 2}) : 0 ) ",
              "values": []
            },
            {
              "name": "maxVolume",
              "displayName": "נפח מקסימלי",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "maxVolume",
              "transformFunction": "(value) => parseFloat( value?.toLocaleString(undefined, { maximumFractionDigits: 2}) ) ",
              "values": []
            },
            {
              "name": "volumePercent",
              "displayName": "ניצול נפח",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "volumePercent",
              "transformFunction": "(value)=> value?  value?.toLocaleString(undefined, { maximumFractionDigits: 2})   + '%':''",
              "values": []
            },
            {
              "name": "routeStartTime",
              "displayName": "שעת התחלה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "routeStartTime",
              "transformFunction": "(time) => { let hours = Math.floor(time); let minutes = Math.round((time - hours) * 60); hours = hours < 10 ? '0' + hours : hours; minutes = minutes < 10 ? '0' + minutes : minutes; return hours + ':' + minutes; }",
              "values": []
            },
            {
              "name": "routeEndTime",
              "displayName": "שעת סיום",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "routeEndTime",
              "transformFunction": "(time) => { let hours = Math.floor(time); let minutes = Math.round((time - hours) * 60); hours = hours < 10 ? '0' + hours : hours; minutes = minutes < 10 ? '0' + minutes : minutes; return hours + ':' + minutes; }",
              "values": []
            },
            {
              "name": "time",
              "displayName": "שעות עבודה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "time",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "weight",
              "displayName": "משקל כולל של המשימות",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 350,
              "groupable": true,
              "filterable": true,
              "accessKey": "weight",
              "transformFunction": "(value)=>  value?.toLocaleString(undefined, { maximumFractionDigits: 2}) ?? '0' ",
              "values": []
            }
          ],
          "query": {
            "request": {
              "url": "",
              "method": "GET/POST",
              "body": {},
              "headers": {
                "": ""
              }
            },
            "existing": {
              "getDataFunction": "()=>planMgrService.getPlanData()",
              "flatFormula": "",
              "func": "(data) => dataExplorerTransformationService.transformPlanDataToFleet(data)",
              "parameters": []
            }
          },
          "export": {
            "function": "(target, field, rowsSearchPartials, value) => planMgrService.setPLanItem(target, field, rowsSearchPartials, value)",
            "columns": [],
            "fieldsMap": []
          },
          "actions": []
        },
        {
          "id": 13,
          "name": "fleet2",
          "displayName": "צי",
          "aggregation": [],
          "views": [
            {
              "id": 1,
              "displayName": "נהגים",
              "sortBy": [],
              "groupBy": [],
              "columnOrder": [],
              "columnVisibility": {},
              "filterBy": []
            }
          ],
          "filters": [],
          "columns": [
            {
              "name": "id",
              "displayName": "מזהה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "id",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "name",
              "displayName": "שם",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "name",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "phone",
              "displayName": "טלפון",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "phone",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "shiftStart",
              "displayName": "ת. משמרת",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "shiftStart",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "shiftEnd",
              "displayName": "ס. משמרת",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "shiftEnd",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "customFields",
              "displayName": "שדות",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "customFields",
              "transformFunction": "(value) => JSON.stringify(value)",
              "values": []
            }
          ],
          "query": {
            "request": {
              "url": "",
              "method": "GET/POST",
              "body": {},
              "headers": {
                "": ""
              }
            },
            "existing": {
              "getDataFunction": "()=>planMgrService.getPlanData()",
              "flatFormula": "",
              "func": "(data) => data?.drivers.map(d=> {return {...d, shiftStart: d.shifts?.[0].start.time, shiftEnd: d.shifts?.[0].end.time}})",
              "parameters": []
            }
          },
          "export": {
            "function": "(target, field, rowsSearchPartials, value) => planMgrService.setPLanItem(target, field, rowsSearchPartials, value)",
            "columns": [],
            "fieldsMap": []
          },
          "actions": []
        },
        {
          "id": 14,
          "name": "fleet3",
          "displayName": "צי",
          "aggregation": [],
          "views": [
            {
              "id": 1,
              "displayName": "משאיות",
              "sortBy": [],
              "groupBy": [],
              "columnOrder": [],
              "columnVisibility": {},
              "filterBy": []
            }
          ],
          "filters": [],
          "columns": [
            {
              "name": "id",
              "displayName": "מזהה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "id",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "plateNumber",
              "displayName": "לוחית",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "plateNumber",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "cf0",
              "displayName": "cf0",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "cf0",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "cf1",
              "displayName": "cf1",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "cf1",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "cf2",
              "displayName": "cf2",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "cf2",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "cf3",
              "displayName": "cf3",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "cf3",
              "transformFunction": "(value) => value",
              "values": []
            },
            {
              "name": "labels",
              "displayName": "תגיות",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "labels",
              "transformFunction": "(value) => value.join(', ')",
              "values": []
            }
          ],
          "query": {
            "request": {
              "url": "",
              "method": "GET/POST",
              "body": {},
              "headers": {
                "": ""
              }
            },
            "existing": {
              "getDataFunction": "()=>planMgrService.getPlanData()",
              "flatFormula": "",
              "func": "(data) => data?.trucks.map(t=> {return {...t, cf0: t.customFields?.[0].value, cf1: t.customFields?.[1].value, cf2: t.customFields?.[2].value, cf3: t.customFields?.[3].value}})",
              "parameters": []
            }
          },
          "export": {
            "function": "(target, field, rowsSearchPartials, value) => planMgrService.setPLanItem(target, field, rowsSearchPartials, value)",
            "columns": [],
            "fieldsMap": []
          },
          "actions": []
        },
        {
          "id": 3,
          "name": "movement",
          "displayName": "העברות",
          "aggregation": [],
          "views": [
            {
              "id": 1,
              "displayName": "מחסנים",
              "sortBy": [
                {
                  "id": "score",
                  "desc": true
                }
              ],
              "groupBy": [],
              "columnOrder": [],
              "columnVisibility": {},
              "filterBy": []
            }
          ],
          "filters": [],
          "columns": [
            {
              "name": "orderId",
              "displayName": "מס' הזמנה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "orderId",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "customerName",
              "displayName": "לקוח",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "customerName",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "from",
              "displayName": "מאיפה",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "from",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "to",
              "displayName": "לאן",
              "dataType": "text",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "to",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "score",
              "displayName": "חוזק המלצה",
              "dataType": "float",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "score",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "volume",
              "displayName": "משטחים",
              "dataType": "int",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "volume",
              "transformFunction": "",
              "values": []
            },
            {
              "name": "weight",
              "displayName": "משקל",
              "dataType": "int",
              "visible": true,
              "editable": false,
              "sortable": true,
              "columnWidth": 150,
              "groupable": true,
              "filterable": true,
              "accessKey": "weight",
              "transformFunction": "",
              "values": []
            }
          ],
          "query": {
            "request": {
              "url": "",
              "method": "GET/POST",
              "body": {},
              "headers": {
                "": ""
              }
            },
            "existing": {
              "getDataFunction": "()=>planMgrService.getPlanData()",
              "flatFormula": "",
              "func": "(data) => { const results = (() => { function createVisitsMap(visits) { const visitsMap = new Map(); for (const visit of data.visits) { visitsMap.set(visit.id, visit); } return visitsMap; } function extractNearWarehousePoints(data, visitsMap) { if (!visitsMap?.size || !data?.routes?.length || !data?.visits?.length) return []; const results = []; let nearByPoints = createNearWarehouses(); for (const route of data.routes){ if (!route.steps?.length) continue; for (const step of route.steps) { if (!step.visitId || (step.type !== 'dropoff' && step.type !== 'pickup')) continue; const visit = visitsMap.get(step.visitId); if (!visit) continue; if (step.type === 'dropoff') { if (nearByPoints.warehouseA.address && nearByPoints.warehouseB.address) results.push(nearByPoints); nearByPoints = createNearWarehouses(); continue; } if ( !nearByPoints.warehouseA.address || nearByPoints.warehouseA.address === visit.pickup.address ){ nearByPoints.warehouseA.address = visit.pickup.address; nearByPoints.warehouseA.visits.push(visit); continue; } if ( !nearByPoints.warehouseB.address || nearByPoints.warehouseB.address === visit.pickup.address ){ nearByPoints.warehouseB.address = visit.pickup.address; nearByPoints.warehouseB.visits.push(visit); continue; } } } return results; } function generateResults(nearWarehousePoints, visitsMap) { if (!visitsMap?.size || !nearWarehousePoints?.length) return []; const results = []; for (const nearWarehousePoint of nearWarehousePoints) { if (!nearWarehousePoint.warehouseA || !nearWarehousePoint.warehouseB) continue; let warehouseFromItemsCount = nearWarehousePoint.warehouseA.visits.reduce((acc, visit) => acc + visit.items.length, 0); let warehouseToItemsCount = nearWarehousePoint.warehouseB.visits.reduce((acc, visit) => acc + visit.items.length, 0); let warehouseFrom, warehouseTo; if (warehouseFromItemsCount < warehouseToItemsCount) { warehouseFrom = nearWarehousePoint.warehouseA; warehouseTo = nearWarehousePoint.warehouseB; } else { warehouseFrom = nearWarehousePoint.warehouseB; warehouseTo = nearWarehousePoint.warehouseA; const tempWarehouseAItemsCount = warehouseFromItemsCount, tempWarehouseBItemsCount = warehouseToItemsCount; warehouseFromItemsCount = tempWarehouseBItemsCount; warehouseToItemsCount = tempWarehouseAItemsCount; } for (const visit of warehouseFrom.visits) { if (!visit.items?.length) continue; const score = calcScore(warehouseFromItemsCount, warehouseToItemsCount); for (const order of visit.items) { const item = createRawObject(); item.orderId = order.orderId; item.customerName = order.customerName; item.from = warehouseFrom.address; item.to = warehouseTo.address; item.score = score; item.volume = order.volume; item.weight = order.weight; results.push(item); } } } return results; } function calcScore(warehouseFromItemsCount, warehouseToItemsCount) { const total = warehouseFromItemsCount + warehouseToItemsCount; return parseFloat((warehouseToItemsCount / total).toFixed(2)); } function createNearWarehouses(){ return { warehouseA: { address: '', visits: [] }, warehouseB: { address: '', visits: [] } } } function createRawObject() { return { 'orderId': '', 'lineId': 1, 'customerName': '', 'from': '', 'to': '', 'score': 1, 'volume': 0, 'weight': 0, } } function calcResults(data){ if (!data?.routes?.length || !data?.visits?.length) return []; const visitsMap = createVisitsMap(); const nearWarehousePoints = extractNearWarehousePoints(data, visitsMap); if (!nearWarehousePoints.length) return []; return generateResults(nearWarehousePoints, visitsMap); } return { get: calcResults } })(); return results.get(data); }",
              "parameters": []
            }
          },
          "export": {
            "function": "(target, field, rowsSearchPartials, value) => planMgrService.setPLanItem(target, field, rowsSearchPartials, value)",
            "columns": [],
            "fieldsMap": []
          },
          "actions": []
        }
      ]
    },
    "forklift": {
      "appId": "forklift"
    },
    "lock": {
      "appId": "lock",
      "group": "Jafora"
    },
    "sidebar": {
      "appId": "sidebar",
      "menu": [
        {
          "id": "data-explorer",
          "link": "/data-explorer",
          "text": "data-explorer",
          "isHidden": true
        },
        {
          "id": "forklift",
          "link": "/forklift",
          "text": "forkliftr",
          "isHidden": true
        },
        {
          "id": "config",
          "link": "/config",
          "text": "config",
          "isHidden": true
        },
        {
          "id": "erp",
          "order": 70,
          "link": "/erp",
          "text": "ERP",
          "icon": "icon-crm",
          "size": "icon-large"
        }
      ]
    }
  },
  "categories": [
    {
      "id": "77edb8c9-46c3-467b-b9ee-0828ff9ac670",
      "name": "סניף 20",
      "value": "20",
      "overrideConfig": {
        "planner": {
          "filters": {
            "defaultPreset": "20"
          },
          "fleet": {
            "defaultFleetData": {
              "defaultTruckSegment": "משאית 20",
              "defaultDriverSegment": "נהג 20"
            }
          }
        }
      }
    },
    {
      "id": "35eaeb99-e249-4b02-9b7f-c44f4cfddbf8",
      "name": "סניף 30",
      "value": "30"
    },
    {
      "id": "fbeb03fc-383d-4553-a8a4-e4dfb8c017fb",
      "name": "סניף 60",
      "value": "60"
    },
    {
      "id": "1a7f356c-0780-4bbc-828b-06cba9b609ab",
      "name": "סניף 70",
      "value": "70"
    }
  ],
  "regions": [
    {
      "name": "צפון",
      "points": "35.29472397463329,33.10724193753326,745.2343536927601 35.20906826353931,33.09955395321943,731.1489642292603 35.20077726618448,33.08723663338108,717.0635747657603 35.19819493691091,33.07063843070318,713.5422273998854 35.1952169134453,33.06291234197629,710.0208800340104 35.19337684470942,33.04881712810699,702.9781853022604 35.18858525164505,33.02187052147926,688.8927958387605 35.18229656247756,33.01004054087785,688.0124589972918 35.17298380040324,32.98494918663445,687.132122155823 35.17925057536532,32.97579060103207,685.3714484728854 35.19346284500021,32.97428683255733,681.8501011070106 35.23317320974795,32.95792860565972,674.8074063752606 35.22392692969094,32.94476996924754,660.7220169117606 35.21464959391803,32.92671687871862,632.5512379847609 35.20523297656504,32.91295065568688,604.380459057761 35.22685870846715,32.87810610530219,576.2096801307612 35.22359935976018,32.86533333351163,519.8681222767616 35.21485654258634,32.85413355833104,518.9877854352928 35.21902032646994,32.84690880129453,518.1074485938242 35.20749937099391,32.84259532533783,516.3467749108868 35.19348145112295,32.84080636419191,512.8254275450117 35.19462695664315,32.83169508234754,505.7827328132616 35.20359939720421,32.82746380200344,502.2613854473866 35.21038844432242,32.80206904682873,498.7400380815116 35.21367029279414,32.79405770851066,491.6973433497617 35.20276063427698,32.7871262376519,484.6546486180117 35.1846889847418,32.78492045241945,477.6119538862618 35.16044153797957,32.73127065648364,463.5265644227619 35.14213881674321,32.68183635260776,407.1850065687623 35.13041352032505,32.63264939909581,393.0996171052624 35.11684283333494,32.60437762787286,379.0142276417625 35.10582972247667,32.57930994039233,350.8434487147628 35.22372011918144,32.55086993054706,294.5018908607632 35.38302608560538,32.44294292423078,86.76593653654255 35.41158222439473,32.42338789172364,34.8319479554874 35.43788957025076,32.40717239134793,-17.10204062556776 35.47058632863714,32.3582735045487,-30.08553777083154 35.50166112252996,32.31035023151984,-43.06903491609533 35.56446998629084,32.30247462671274,-56.05253206135913 35.56927701587531,32.36932787988188,-69.03602920662291 35.56158928888844,32.43237956424249,-120.9700177876781 35.94048059169126,32.72028633633548,268.9813885734175 35.91436919610884,33.28379156609159,1211.146033268921 35.53408797938651,33.31152593960972,499.8001811460399 35.49033423309657,33.09331670176454,622.5172674194 35.29472397463329,33.10724193753326,745.2343536927601"
    },
    {
      "name": "חיפה נהריה",
      "points": "34.90233173788024,32.62782309272252,0 35.10634427231259,32.57866652416006,0 35.13334847174111,32.64044137236957,0 35.18513368113647,32.78614998690998,0 35.20485291718897,32.78624247358576,0 35.21711024781304,32.7946016862964,0 35.20374905439042,32.82791527232178,0 35.19318202661053,32.83253027708456,0 35.19418280966541,32.84076650644393,0 35.22033285695522,32.84599009910651,0 35.23060924181011,32.87558422712713,0 35.20634265745642,32.91446070396996,0 35.23356392989238,32.95770003563076,0 35.19254104251031,32.97462501439755,0 35.17769627669004,32.97524213465929,0 35.17243236499787,32.98740461332556,0 35.20995286129895,33.09981433394807,0 35.09912656485648,33.10166814555981,0 34.93854933446696,32.82711336884682,0 34.90233173788024,32.62782309272252,0"
    },
    {
      "name": "מרכז צפוני",
      "points": "34.90285511734577,32.62819760987605,5.302948870016042 34.81257467741726,32.21091451915878,8.086337710649161 34.92823325072134,32.20477768071959,12.55865429907979 34.95687179539056,32.19905587705639,17.03097088751041 34.95604373318108,32.19270601836374,19.26712918172572 34.95749735876079,32.18446463057925,21.50328747594104 34.96022042708472,32.16873428924811,25.97560406437166 34.96546183075752,32.17472489478531,28.21176235858697 34.98780861662141,32.18041690209916,30.44792065280229 35.00183122700839,32.18595272136595,34.92023724123291 35.01804235648665,32.18794392895283,39.39255382966354 35.03299745324318,32.18322565644814,43.86487041809416 35.0112655566446,32.23039226670939,79.64340312553917 35.06214969703631,32.295239868598,86.57376814678234 35.19218932796228,32.42464118773078,93.50413316802552 35.22399893951439,32.55120742189234,107.3648632105119 34.90285511734577,32.62819760987605,5.302948870016042"
    },
    {
      "name": "השרון",
      "points": "34.78926741449362,32.14410185457425,5.429578449130091 34.82935139753081,32.13677218221575,48.92534509026847 34.85521317355967,32.1247499049044,38.0376532286262 34.87753784751765,32.11679897850854,25.28977845264085 34.89252885296291,32.1225942258805,12.34467050823529 34.93708842083024,32.11614785539351,25.71134413796106 34.95116233885745,32.13114902969581,35.35800446160102 34.95835061005637,32.13828024663551,40.181334623421 34.96302486471824,32.1465797586735,45.00466478524098 34.96026127225293,32.16784061623166,48.51031214515356 34.95929137183317,32.17307258627069,52.2651824337526 34.95607493097108,32.19472189132361,48.66902840435882 34.95715072084906,32.19923900267383,45.07287437496505 34.92905198315901,32.20519284526561,69.08164479639115 34.81210367515908,32.21113637441213,17.83216879357015 34.79597176059896,32.17780292208067,11.63087362135012 34.78926741449362,32.14410185457425,5.429578449130091"
    },
    {
      "name": "שומרון",
      "points": "35.24244865116174,32.09617935822813,111.674732754093 35.14392714626937,32.09362832064736,143.401994134657 35.06139964215325,32.06246983231894,159.265624824939 35.04708334259099,32.05731442116991,167.1974401700801 35.00124474336596,32.05081117879107,175.1292555152211 35.0038711691451,32.01948904217751,386.7541684960068 34.98452183592102,31.97303867926222,598.3790814767925 35.04986839409847,31.97092016841514,591.0001360414467 35.07163915047868,31.96672377008481,583.6211906061008 35.07474462121674,31.96172959909394,568.8632997354089 35.04847837613062,31.94427488654933,554.105408864717 35.05656338563037,31.93459565411353,553.1830406852989 35.05674677122596,31.92043712714301,552.2606725058806 35.0429110289472,31.90561651480086,551.3383043264623 35.06692440149118,31.89028790425138,550.415936147044 35.09777159344025,31.88833560788002,546.7264634293711 35.18645529025499,31.88019580065291,539.3475179940251 35.27205402552813,31.84362439364743,480.3159545112577 35.40535669390447,31.83056471615824,362.2528275457228 35.43209115478982,31.88875980487677,126.1265736146531 35.57506136675402,31.87867710682282,-346.1259342474863 35.56381992041577,32.30286919271516,-265.4551504593043 35.53504299018821,32.30695875574037,-225.1197585652132 35.50250494421233,32.31080269066051,-184.7843666711221 35.43825100648814,32.40767680426504,114.8831900495671 35.22418176687931,32.55171792660902,414.5507467702565 35.19196608345412,32.42604063235618,357.3657720593134 35.06203759632734,32.29535287225747,328.7732847038419 35.01120577886747,32.23041540660299,300.1807973483704 35.04292395801941,32.16134480544577,185.8108479264843 34.99180582640254,32.14760289053856,167.2768191333865 35.12160033808805,32.15806245838888,148.7427903402886 35.24244865116174,32.09617935822813,111.674732754093"
    },
    {
      "name": "תל אביב",
      "points": "34.78879480932852,32.14389328377753,67.33573840475823 34.72666387938288,32.00487332555962,5.886561015701865 34.80230381350401,31.99667478351866,87.77951553574837 34.81107143073812,32.0070511602304,185.8960103061237 34.82063792275854,32.01902826582993,194.6481879745943 34.82876418910089,32.02929939441495,203.4003656430649 34.82980335443105,32.0376664559393,220.9047209800061 34.82994179222402,32.04656664689276,176.1211104571013 34.83822593004365,32.06448976264317,153.7293051956489 34.84308366551878,32.07278850083831,142.5334025649227 34.84575030751642,32.08566073940383,136.9354512495595 34.84592712572054,32.09536464939924,134.136475591878 34.85082641931145,32.11310410570504,132.7369877630372 34.85246313273693,32.11987856491952,132.0372438486168 34.85571253082375,32.12466562571813,131.3374999341964 34.83354705245898,32.1353853358628,81.62074462506718 34.81262851748146,32.1386355316321,31.9039893159379 34.78879480932852,32.14389328377753,67.33573840475823"
    },
    {
      "name": "ירושלים",
      "points": "34.89097457587891,31.90261641219027,84.21586604811903 34.85501723855744,31.68903916076555,202.9775555474272 34.93679338229489,31.65741389705908,73.68489119719511 35.14989088410652,31.58383977803879,-55.60777315303699 35.32999806712592,31.75247239064769,-184.9004375032691 35.39665635367472,31.80840051114133,-314.1931018535012 35.40516239904053,31.83154071388494,-342.8024955223832 35.27092734135369,31.84539448593764,-311.0349863477348 35.17658530182518,31.88175871037728,-295.1512317604105 35.12595704673687,31.88698999168545,-279.2674771730863 35.06684186592572,31.89048969018593,-278.7711098422324 35.04314492780783,31.90517418744016,-278.2747425113785 35.05657452028699,31.92047335268683,-277.2820078496708 35.05680547534954,31.9347220825206,-275.2965385262552 35.04869492506904,31.94399078005404,-271.3255998794242 35.06503327521736,31.95631592739128,-263.383722585762 35.07457364146853,31.96179955239723,-247.4999679984378 35.07148393875213,31.96650549059627,-215.7324588237893 35.05005761049066,31.97098034656092,-88.66242212519541 34.98350071588786,31.97368908846697,165.4776512719924 34.93671885781159,31.95946158499059,124.8467586600557 34.89097457587891,31.90261641219027,84.21586604811903"
    },
    {
      "name": "פתח תקווה - אריאל",
      "points": "34.84681247021833,32.09973409819331,30.32721100986913 34.84511363852211,32.08081618306358,42.53129677488484 34.8297005696853,32.04978403072875,53.75620904029358 34.82969873162997,32.03186157523936,30.02038543178319 34.82113370595873,32.01828532205599,30.58921065386185 34.86287608458701,31.99067523091327,33.10396288041762 34.87716123794124,31.99600927128045,31.88266920509655 34.89259176887951,31.98292490230202,35.72611406185789 34.93712853325884,31.95967330022995,85.80649464616361 34.98444003852092,31.97275480553116,190.0343070253644 35.00558349253378,32.0206427965789,212.3584014784227 35.00277982685344,32.05113314987799,201.7545927355341 35.04544811853785,32.05635227807559,314.0481067196778 35.1450783358148,32.09427438187249,459.4829337098454 35.24144495368473,32.0964735295983,488.723708096933 35.12225445124175,32.15783737728096,300.0858380546647 34.9904158473513,32.14758449958163,120.6039543850847 35.04401238007191,32.16280937136769,269.3852410387223 35.03439519690976,32.1837048844172,228.8363769648282 35.01902200070587,32.18816586786902,180.6618206803937 35.00475411195392,32.18678778184238,145.4857343237239 34.98594343815707,32.17986421200135,107.2156529202954 34.96530538553461,32.1738573506411,68.94557151686686 34.95957208787242,32.16803579195251,71.6348041186653 34.96243180918983,32.14673927446427,46.29654468788843 34.95804409664635,32.13819069858714,42.42286120243482 34.95119366756714,32.13109830810404,38.54917771698121 34.93723086390742,32.11670475483068,30.801810746074 34.91662761367355,32.11913414009179,30.0413696244598 34.89201646142739,32.12301358929103,31.0440631602911 34.87713612625046,32.11671004431832,30.35048636143323 34.85652926048383,32.12542892489117,34.82204919699263 34.84681247021833,32.09973409819331,30.32721100986913"
    },
    {
      "name": "יבנה-ראשון-לוד",
      "points": "34.65185222417444,31.86278834007316,-9.584652969815865 34.87583927389332,31.80395980455371,127.68688127092 34.89043802959817,31.90378712612058,85.40358094012134 34.93610449632443,31.95931510595129,81.35503636358951 34.87862147033223,31.99590664358089,31.94060165430645 34.86273651277794,31.99085380789821,32.9707243554037 34.82104339527965,32.01950395643903,30.53254162289264 34.80185977787423,31.99645125140557,43.24468435518297 34.72635750363475,32.00493880680384,-8.150185661382473 34.65185222417444,31.86278834007316,-9.584652969815865"
    },
    {
      "name": "אשקלון-אשדוד",
      "points": "34.53095294136171,31.65067542309815,10.82173429880171 34.72403799948894,31.64740929935813,90.57069817802324 34.75577430105508,31.62680208871443,92.7147622362708 34.77254898669278,31.63793323595678,93.37919462707004 34.80520630029169,31.63162985541873,130.6639834225608 34.80523550657702,31.61420265085007,173.7083285634459 34.88068691254546,31.60321105562816,286.4185603813864 34.92348128652633,31.62387333845799,367.0012730761858 34.96253879051143,31.60325010644155,374.5926651077008 34.99231448767994,31.63969748043085,416.3560125230846 34.85833371795863,31.68959175026891,165.9759743180793 34.87886506852145,31.80306906591852,122.7582952075499 34.6501370354899,31.86310833592378,9.370247015971271 34.59863937121747,31.75130526529949,10.09599065738649 34.53095294136171,31.65067542309815,10.82173429880171"
    },
    {
      "name": "דרום",
      "points": "34.2220462621633,31.32610620717708,-39.09068915039531 34.44248863728929,30.7797122453181,406.9000068163932 35.41478377319106,30.91393803953111,-275.6089222282296 35.58176426127157,31.79215891363437,-373.7779574001504 35.57360004199376,31.87994404588306,-349.6951439648464 35.43563358080057,31.88916645530825,-346.6847922854334 35.40477100340603,31.83143199127328,-343.6744406060204 35.39652274698125,31.8081295736124,-337.6537372471944 35.35302464034979,31.77747372364327,-325.6123305295424 35.15058290984817,31.58361959974286,-277.4467036589344 34.99087531686122,31.63881822898797,-229.2810767883264 34.96094248769086,31.60342536393672,-205.1982633530224 34.9501584285084,31.6132722600102,-193.1568566353704 34.92505868740242,31.62496450055088,-187.1361532765444 34.89103427782796,31.61548271968159,-184.1258015971314 34.88218723448116,31.60346092068285,-181.1154499177184 34.83603288720958,31.60789213485554,-132.9498230471104 34.80652937862478,31.61423953404222,-84.78419617650246 34.80494473242666,31.63146090129376,-60.70138274119847 34.77758670830509,31.63717992688239,-57.69103106178547 34.77303729246944,31.63830030744455,-56.93844314193221 34.76930504171333,31.63663541055866,-56.18585522207896 34.75664021453642,31.62751860863191,-54.68067938237247 34.74427863201748,31.63430240483864,-48.65997602354647 34.72851508266865,31.64668376926528,-42.63927266472047 34.7233652766655,31.64797655855093,-41.13409682501398 34.7169473250061,31.6471555719162,-39.62892098530748 34.70752129900248,31.64808710033994,-38.12374514560099 34.69379029744777,31.64825059895668,-37.37115722574774 34.68030058677906,31.64895796203873,-36.61856930589448 34.52717912217619,31.65150345500573,11.5470575647135 34.4616834844775,31.56132492956616,-1.112379114063701 34.38399388937057,31.48001156800117,-13.77181579284091 34.30184850011684,31.40131493451251,-26.43125247161811 34.2220462621633,31.32610620717708,-39.09068915039531"
    },
    {
      "name": "אילת",
      "points": "34.89738604029423,29.4761918483838,15.82524765454994 34.98944402632999,29.55396211207476,34.10983769454307 35.41490672092725,30.91621609817573,-525.7491017972076 34.43908366896542,30.78022904601212,308.911224787459 34.53342080041622,30.40916165184092,235.6397305042318 34.73318811716881,30.13922771899027,162.3682362210045 34.89738604029423,29.4761918483838,15.82524765454994"
    }
  ]
}



<li data-test-id="TaskEditor-TaskEditorBar-TaskWeightVolume-WeightEditBox" class="_status-bar-wight_qptoi_2"><span class="icon-weight icon-small icon-gray"></span><span class=" font-style-light">משקל</span><span class="font-style-bold">1,936</span></li>