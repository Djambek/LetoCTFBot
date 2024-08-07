import React from 'react';
import styles from './App.module.css';
import { List, Accordion, Blockquote } from '@telegram-apps/telegram-ui';
import { get_events } from './api.jsx';

const AccordionSummary = Accordion.Summary;
const AccordionContent = Accordion.Content;
class EventView extends React.Component {
	constructor(props) {
		super(props);
		this.state = { bent: true, name: props.name, description: props.description }
	}

	render() {
		let e = '';
		if(!this.state.bent)
			e = "1";
  	return (
	    <Accordion expanded={e} onChange={() => this.setState((t) => { bent: !t.bent })}>
    	  <AccordionSummary>
				  { this.state.name }
    	  </AccordionSummary>
      	<AccordionContent>
			  	<List>
						<Blockquote> {this.state.description} </Blockquote>
					</List>
  	    </AccordionContent>
    	</Accordion>
	  );}
};

class Events extends React.Component {
  constructor(props) {
    super(props);
    let e = get_events();
    this.state = {
      event_data: e,
      app: props.app,
    };
  }

  render() {
    let events = this.state.event_data.map((e, i) => (
      <EventView events={this} app={this.state.app} {...e} />
    ));
    return (
      <List>
	{ events }
      </List>
    );
  }
}

export default Events;

