import React from 'react';

import '@telegram-apps/telegram-ui/dist/styles.css';
import styles from './App.module.css';
import { InlineButtons } from '@telegram-apps/telegram-ui';
import { use_item, get_items } from './api.jsx';

const InlineButtonsItem = InlineButtons.Item;
const InventoryItem = (props) => {
	let heart = <i className={ "icon-heart " + styles.heal}> </i>;
	let sword = <span className={ "material-symbols-outlined " + styles.sword + ' ' + styles.damage }> swords </span>;
	
	let icon = null; let color = null;
	if(props.effect < 0) {
		color = styles.damage;
		icon = sword;
	} else {
		color = styles.heal;
		icon = heart;
	}
	
	let confirm = null, confirm_2 = null;
	if(props.confirm_stage[props.idx] === 'select') {
		confirm = (<InlineButtons mode="plain">
			<InlineButtonsItem
				onClick={() => {
					let next = [...props.inv.state.confirm_stage];
					next[props.idx] = 'confirm';
					props.inv.setState({confirm_stage: next});
				}}
			>
				<span className={"material-symbols-outlined " + styles.sword}>
					add_circle
				</span>
				Use
			</InlineButtonsItem>
		</InlineButtons>);
		confirm_2 = "";
	} else if(props.confirm_stage[props.idx] === 'confirm') {
		confirm = (<InlineButtons mode="plain">
			<InlineButtonsItem
				onClick={() => {
					let next = [...props.inv.state.confirm_stage];
					next[props.idx] = 'select';
					props.inv.setState({confirm_stage: next});
				}}
			>
				<span className={"material-symbols-outlined " + styles.sword}>
					close
				</span>
				Cancel
			</InlineButtonsItem>
		</InlineButtons>);
		confirm_2 = (<InlineButtons mode="plain">
			<InlineButtonsItem
			onClick={() => { 
				use_item(props.id); 
				let items = get_items();
				props.app.setState({items: items});
				props.app.setState({page: props.app.inventory()});
				location.reload();
				props.app.forceUpdate();
			}}>
				<span className={"material-symbols-outlined " + styles.sword}>
					check
				</span>
				Confirm
			</InlineButtonsItem>
		</InlineButtons>);
	}
	

	return (<tr className={styles.invdivider}>
		<td style={{ 'textAlign': 'left', width: '38%' }} className={styles.heal_icon}>{props.name}</td>
		<td style={{ 'textAlign': 'center', 'verticalAlign': 'middle', width: '15%' }} className={color}>
			<span>{props.effect} </span>
			{ icon }
		</td>
		<td style={{ 'justifyContent': 'right', width: '47%' }}> 
			<InlineButtons style={{ justifyContent: 'right'}}>
				{ confirm_2 }
				{ confirm }
			</InlineButtons>
		</td>
	</tr>);
}

class Inventory extends React.Component {
	constructor(props) {
		super(props);

		const items = get_items()

		this.state = {
			items: items,
			confirm_stage: items.map((_, __) => ('select')),
			app: props.app
		};
	}

	render() {
		let table = this.state.items.map((e, i) => (
			<InventoryItem app={this.state.app} inv={this} idx={i} key={i} {...e} {...this.state}> </InventoryItem>
		));

		return (	
			<div
				style={{background:'var(--dark)', padding: '2%'}}
			>
				<table style={{ 'margin': '0 3%', width: '94%' }}>
					<tbody>
						{ table }
					</tbody>
				</table>
			</div>
		);
	}	
}

export default Inventory;

